"""
kmin-test check: does removing extrap_kmin and raising the k-floor to
10^-4.85 change the DES posteriors?  If des_*_mnu_kmin ~ des_*_mnu, the
k-grid change is exonerated and the remaining width vs the published
chains is attributable to the shear-ratio (SR) likelihood + samplers.

Run:  conda activate plot_dist && python compare_kmin.py
"""
from pathlib import Path
import os
import sys

os.chdir(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path("../compare_desy3").resolve()))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from getdist import loadMCSamples, plots

matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['savefig.bbox'] = 'tight'
for k in ['axes.titlesize', 'axes.labelsize', 'legend.fontsize',
          'xtick.labelsize', 'ytick.labelsize']:
    matplotlib.rcParams[k] = 10

DES = "../../cocoa/Cocoa/projects/des_y3/chains/"
COLORS = ['#7386BE', '#FFAF4C']

CH = {
    "y1_mnu":      DES + "des_y1_mnu_mcmc/",
    "y1_mnu_kmin": DES + "des_y1_mnu_kmin_mcmc/",
    "y3_mnu":      DES + "des_y3_mnu_mcmc/",
    "y3_mnu_kmin": DES + "des_y3_mnu_kmin_mcmc/",
}


def load(fp, settings={'ignore_rows': 0.2, 'contours': [0.68, 0.95]}):
    s = loadMCSamples(fp, settings=settings)
    p = s.getParams()
    s.addDerived(p.sigma8 * (p.omegam / 0.3) ** 0.5, 'S8', label='S_8')
    return s


def stat(sample, p):
    st = sample.getMargeStats().parWithName(p)
    m = st.mean
    return m, st.limits[0].upper - m, m - st.limits[0].lower


def compare(tag, k_mnu, k_kmin, savepath):
    s_mnu, s_kmin = load(CH[k_mnu]), load(CH[k_kmin])
    print(f"\n=== {tag} ===")
    print(f"{'param':6s} {'mnu (extrap, -4.90)':28s} {'kmin (no extrap, -4.85)':28s} shift/sigma")
    for p in ['omegam', 'sigma8', 'S8', 'mnu']:
        try:
            m0, up0, lo0 = stat(s_mnu, p)
            m1, up1, lo1 = stat(s_kmin, p)
            sig = 0.5 * (up0 + lo0)
            dshift = (m1 - m0) / sig if sig > 0 else float('nan')
            print(f"{p:6s} {m0:.4f} +{up0:.4f} -{lo0:.4f}   "
                  f"{m1:.4f} +{up1:.4f} -{lo1:.4f}   {dshift:+.2f}")
        except Exception:
            pass

    g = plots.get_subplot_plotter(subplot_size=3.2)
    g.settings.alpha_filled_add = 0.5
    g.plot_2d([s_mnu, s_kmin], ['omegam', 'S8'],
              filled=True, colors=COLORS,
              legend_labels=[f'{tag} mnu (extrap, floor -4.90)',
                             f'{tag} mnu_kmin (no extrap, floor -4.85)'])
    ax = g.get_axes()
    handles = [Patch(facecolor=c, edgecolor=c, alpha=0.6, label=l)
               for c, l in zip(COLORS,
                               [f'{tag} mnu (extrap, floor -4.90)',
                                f'{tag} mnu_kmin (no extrap, floor -4.85)'])]
    ax.legend(handles=handles, fontsize=8, loc='upper right', frameon=False)
    ax.text(0.05, 0.05, r'$\Lambda$CDM - ShearOnly', transform=ax.transAxes, fontsize=9)
    g.export(savepath, dpi=300)
    print(f'saved {savepath}')


if __name__ == '__main__':
    compare('DES_Y1', 'y1_mnu', 'y1_mnu_kmin', 'kmin_check_DES_Y1.jpg')
    compare('DES_Y3', 'y3_mnu', 'y3_mnu_kmin', 'kmin_check_DES_Y3.jpg')
