"""
Chain comparisons for the mnu-marginalization campaign (July 2026).

Follows the conventions of ../compare_desy3/plot.ipynb:
  (1) roman vs roman_mnu      -> effect of marginalizing mnu (+ kmin/extrap_kmin change)
  (2) des vs des_mnu          -> effect of marginalizing mnu on DES real data
  (3) des_mnu vs published DES-> our COCOA MCMC vs the DES collaboration MCMC
  (4) roman_mnu vs des        -> Roman-Y1 constraining power vs DES
Plus mnu 1D marginals and fixed-vs-marginalized triangle plots.

Run:  conda activate plot_dist && python compare_mnu.py
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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator

from utils import load_chain_parameters
from getdist import loadMCSamples, plots, mcsamples

# ---------------- plot style (copied from compare_desy3/plot.ipynb) ----------------
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['xtick.bottom'] = True
matplotlib.rcParams['xtick.top'] = False
matplotlib.rcParams['ytick.right'] = False
matplotlib.rcParams['ytick.major.size'] = 6
matplotlib.rcParams['ytick.major.width'] = 1.2
matplotlib.rcParams['ytick.minor.size'] = 3
matplotlib.rcParams['ytick.minor.width'] = 0.8
matplotlib.rcParams['axes.edgecolor'] = 'black'
matplotlib.rcParams['axes.linewidth'] = '1.0'
matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['grid.linewidth'] = '0.0'
matplotlib.rcParams['grid.alpha'] = '0.18'
matplotlib.rcParams['grid.color'] = 'lightgray'
matplotlib.rcParams['legend.labelspacing'] = 0.77
matplotlib.rcParams['savefig.bbox'] = 'tight'
matplotlib.rcParams['savefig.dpi'] = 300
for k in ['axes.titlesize', 'axes.labelsize', 'legend.fontsize',
          'legend.title_fontsize', 'xtick.labelsize', 'ytick.labelsize']:
    matplotlib.rcParams[k] = 10

columnwidth = 246 / 72.27

COLORS = ['#FFAF4C', '#9A6289', '#7386BE', '#959596', '#4C9987']
LINESTYLES = ['-', '-.', ':', '--', '--']

# ---------------- chain locations ----------------
ROMAN = "../../cocoa/Cocoa/projects/roman_y1/chains/"
DES = "../../cocoa/Cocoa/projects/des_y3/chains/"
PUB = "../compare_desy3/chains/"

CH = {
    "roman41":      ROMAN + "roman_lsst_41_mcmc/",
    "roman60":      ROMAN + "roman_lsst_60_mcmc/",
    "roman41_mnu":  ROMAN + "roman_lsst_41_mnu_mcmc/",
    "roman60_mnu":  ROMAN + "roman_lsst_60_mnu_mcmc/",
    "desy1":        DES + "des_y1_mcmc/",
    "desy3":        DES + "des_y3_mcmc/",
    "desy1_mnu":    DES + "des_y1_mnu_mcmc/",
    "desy3_mnu":    DES + "des_y3_mnu_mcmc/",
    "desy1_pub":    PUB + "s_l3.txt",
    "desy3_pub":    PUB + "chain_1x2pt_lcdm_SR_maglim.txt",
}

STATS_LINES = []


def DES_LOAD(filepath, settings):
    parameters, weights = load_chain_parameters(filepath, ["omegam", "sigma8"])
    return mcsamples.MCSamples(
        samples=np.array(parameters),
        weights=np.array(weights),
        names=['omegam', 'sigma8'],
        labels=['$\\Omega_m$', '$\\sigma_8$'],
        settings=settings)


def load(filepath, settings={'ignore_rows': 0.2, 'contours': [0.68]}):
    try:
        sample = loadMCSamples(filepath, settings=settings)
    except Exception:
        sample = DES_LOAD(filepath, settings)
    p = sample.getParams()
    s8 = p.sigma8 * (p.omegam / 0.3) ** 0.5
    sample.addDerived(s8, 'S8', label=r'S_8')
    means = sample.getMeans()
    ix = sample.getParamNames().numberOfName('omegam')
    iy = sample.getParamNames().numberOfName('S8')
    sample.addDerived(s8 - means[iy], 'delta_S8', label=r'\Delta S_8')
    sample.addDerived(p.omegam - means[ix], 'delta_omegam', label=r'\Delta \Omega_m')
    pn = sample.getParamNames()
    for par in pn.names:
        if par.name == 'mnu':
            par.label = r'\sum m_{\nu}\,[\mathrm{eV}]'
        if par.name.lower() == 'omegan':
            par.label = r'\Omega_{\nu}'
        if par.name == 'As_1e9':
            par.label = r'10^{9} A_{\rm s}'
    return sample


_cache = {}


def get(key):
    if key not in _cache:
        _cache[key] = load(CH[key])
    return _cache[key]


def print_stats(samples, labels, params=('omegam', 'sigma8', 'S8', 'mnu')):
    for sample, lab in zip(samples, labels):
        for p in params:
            try:
                stat = sample.getMargeStats().parWithName(p)
                if stat is None:
                    continue
                mean = stat.mean
                up = stat.limits[0].upper - mean
                lo = mean - stat.limits[0].lower
                line = f'{lab:24s} {p:8s} = {mean:.4f} +{up:.4f} -{lo:.4f} (68%)'
                print(line)
                STATS_LINES.append(line)
            except Exception:
                pass
    STATS_LINES.append('')


def plot2d(keys, labels, params, savepath, delta=False, annotate=None):
    samples = [get(k) for k in keys]
    n = len(labels)

    g = plots.get_subplot_plotter(subplot_size=columnwidth,
                                  width_inch=columnwidth * 1.1,
                                  subplot_size_ratio=1)
    g.make_figure(nplot=1, nx=1)
    g.settings.tight_layout = False
    g.settings.title_limit = 0
    g.settings.lab_fontsize = 10
    g.settings.legend_fontsize = 10
    g.settings.figure_legend_frame = False
    g.settings.axes_fontsize = 10
    g.settings.axes_labelsize = 10
    g.settings.axis_tick_max_labels = 4
    g.settings.alpha_factor_contour_lines = 3.0

    kwargs = {}
    if delta:
        kwargs['lims'] = [-0.2, 0.2, -0.2, 0.2]
    g.plot_2d(roots=samples, param_pair=params, legend_labels=labels,
              colors=COLORS[:n], ls=LINESTYLES[:n], lws=[2.5] * n,
              alphas=[0.3] * n, filled=[True] * n, ax=(0, 0), **kwargs)

    ax = g.get_axes(ax=(0, 0))
    if delta:
        ax.yaxis.set_major_locator(MultipleLocator(0.05))
        ax.yaxis.set_minor_locator(MultipleLocator(0.025))
        ax.xaxis.set_major_locator(MultipleLocator(0.06))
        ax.xaxis.set_minor_locator(MultipleLocator(0.03))
    if annotate:
        ax.text(x=0.05, y=0.05, s=annotate, transform=ax.transAxes, fontsize=9)

    handles = [Patch(facecolor=c, edgecolor=c, linewidth=2.0, alpha=0.8, label=lab)
               for lab, c in zip(labels, COLORS[:n])]
    g.legend = g.fig.legend(handles, labels, loc='lower center',
                            bbox_to_anchor=(0.55, 0.90), ncol=2,
                            frameon=False, fontsize=10)
    g.extra_artists = [g.legend]
    g.export(savepath, dpi=300)
    print(f'saved {savepath}')
    print_stats(samples, labels)


def plot_mnu_1d(keys, labels, savepath):
    samples = [get(k) for k in keys]
    n = len(labels)
    g = plots.get_subplot_plotter(subplot_size=columnwidth,
                                  width_inch=columnwidth * 1.1)
    g.settings.figure_legend_frame = False
    g.settings.legend_fontsize = 9
    g.plot_1d(samples, 'mnu', colors=COLORS[:n], ls=LINESTYLES[:n], lws=[2.0] * n)
    ax = g.get_axes()
    ax.axvline(0.06, color='k', lw=0.8, ls=':', alpha=0.6)
    ax.text(0.065, 0.05, 'fiducial 0.06 eV', rotation=90, fontsize=7, alpha=0.7)
    handles = [Line2D([0], [0], color=c, ls=l, lw=2.0)
               for c, l in zip(COLORS[:n], LINESTYLES[:n])]
    g.fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.55, 0.90),
                 ncol=2, frameon=False, fontsize=9)
    g.export(savepath, dpi=300)
    print(f'saved {savepath}')


def plot_triangle(keys, labels, params, savepath):
    samples = [get(k) for k in keys]
    n = len(labels)
    g = plots.get_subplot_plotter(width_inch=1.8 * columnwidth)
    g.settings.figure_legend_frame = False
    g.settings.legend_fontsize = 10
    g.triangle_plot(samples, params, filled=True, legend_labels=labels,
                    colors=COLORS[:n], contour_colors=COLORS[:n])
    g.export(savepath, dpi=300)
    print(f'saved {savepath}')


if __name__ == '__main__':
    lcdm_txt = r'$\Lambda$CDM - ShearOnly'

    # (1) Roman fixed-mnu vs marginalized-mnu (also folds in kmin/extrap_kmin change)
    plot2d(['roman41', 'roman41_mnu', 'roman60', 'roman60_mnu'],
           ['ROMAN_41 (fix $m_\\nu$)', 'ROMAN_41 (free $m_\\nu$)',
            'ROMAN_60 (fix $m_\\nu$)', 'ROMAN_60 (free $m_\\nu$)'],
           ['omegam', 'S8'], 'Roman_fix_vs_free_mnu.jpg', annotate=lcdm_txt)

    # (2) DES fixed-mnu vs marginalized-mnu (our COCOA chains, real data)
    plot2d(['desy1', 'desy1_mnu', 'desy3', 'desy3_mnu'],
           ['DES_Y1 (fix $m_\\nu$)', 'DES_Y1 (free $m_\\nu$)',
            'DES_Y3 (fix $m_\\nu$)', 'DES_Y3 (free $m_\\nu$)'],
           ['omegam', 'S8'], 'DES_fix_vs_free_mnu.jpg', annotate=lcdm_txt)

    # (3) our COCOA mnu chains vs the published DES chains
    plot2d(['desy1_mnu', 'desy1_pub'],
           ['DES_Y1_COCOA (free $m_\\nu$)', 'DES_Y1 published'],
           ['omegam', 'S8'], 'COCOA_mnu_4_DES_Y1.jpg', annotate=lcdm_txt)
    plot2d(['desy3_mnu', 'desy3_pub'],
           ['DES_Y3_COCOA (free $m_\\nu$)', 'DES_Y3 published'],
           ['omegam', 'S8'], 'COCOA_mnu_4_DES_Y3.jpg', annotate=lcdm_txt)

    # (4) Roman-Y1 vs DES constraining power, all with mnu marginalized
    plot2d(['roman41_mnu', 'roman60_mnu', 'desy1_mnu', 'desy3_mnu'],
           ['ROMAN_Y1_41', 'ROMAN_Y1_60', 'DES_Y1', 'DES_Y3'],
           ['delta_omegam', 'delta_S8'], 'RomanY1_vs_DES_mnu.jpg',
           delta=True, annotate=lcdm_txt)

    # bonus: mnu marginal posteriors, and fixed-vs-free triangles
    plot_mnu_1d(['roman41_mnu', 'roman60_mnu', 'desy1_mnu', 'desy3_mnu'],
                ['ROMAN_Y1_41', 'ROMAN_Y1_60', 'DES_Y1', 'DES_Y3'],
                'mnu_marginals_1D.jpg')
    plot_triangle(['roman41', 'roman41_mnu'],
                  ['ROMAN_41 (fix $m_\\nu$)', 'ROMAN_41 (free $m_\\nu$)'],
                  ['omegam', 'sigma8', 'S8', 'mnu'], 'triangle_roman41.jpg')
    plot_triangle(['desy3', 'desy3_mnu'],
                  ['DES_Y3 (fix $m_\\nu$)', 'DES_Y3 (free $m_\\nu$)'],
                  ['omegam', 'sigma8', 'S8', 'mnu'], 'triangle_desy3.jpg')

    with open('stats.txt', 'w') as f:
        f.write('\n'.join(STATS_LINES) + '\n')
    print('saved stats.txt')
