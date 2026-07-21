"""
Regenerate every comparison figure in the style of plot.ipynb
(delta_omegam / delta_S8, single 68% contour, 20% burn-in) and write them
all into ./figures/.

Also runs a burn-in sensitivity diagnostic first, so we can see explicitly
whether the 20% burn-in used by plot.ipynb is enough for these chains.

Run on a compute node, e.g.
  srun --account=pi-chihway --partition=caslake --nodes=1 --ntasks=1 \
       --cpus-per-task=12 --time=01:00:00 python make_figures.py
"""
from pathlib import Path
import os
import sys

os.chdir(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path("../compare_desy3").resolve()))
sys.path.insert(0, str(Path(".").resolve()))

import matplotlib
matplotlib.use("Agg")

from plot_utils import compare_chains_single, load, plots, COLORS
from matplotlib.lines import Line2D

FIG = Path("figures")
FIG.mkdir(exist_ok=True)

# local copies (as used by plot.ipynb) for the mnu/kmin/published chains
LOC = "./chains/"
# fixed-mnu chains live next door
OLD = "../compare_desy3/chains/"

CH = {
    "roman41":      OLD + "roman_lsst_41_mcmc/",
    "roman60":      OLD + "roman_lsst_60_mcmc/",
    "roman41_mnu":  LOC + "roman_lsst_41_mnu_mcmc/",
    "roman60_mnu":  LOC + "roman_lsst_60_mnu_mcmc/",
    "y1":           OLD + "des_y1_mcmc/",
    "y3":           OLD + "des_y3_mcmc/",
    "y1_mnu":       LOC + "des_y1_mnu_mcmc/",
    "y3_mnu":       LOC + "des_y3_mnu_mcmc/",
    "y1_kmin":      LOC + "des_y1_mnu_kmin_mcmc/",
    "y3_kmin":      LOC + "des_y3_mnu_kmin_mcmc/",
    # published: s_l3.txt is DES Y1; chain_1x2pt_lcdm_SR_maglim.txt is DES Y3
    "y1_pub":       LOC + "s_l3.txt",
    "y3_pub":       LOC + "chain_1x2pt_lcdm_SR_maglim.txt",
}

STATS = []
DELTA = ['delta_omegam', 'delta_S8']


def burnin_diagnostic():
    print("\n" + "=" * 72)
    print("BURN-IN SENSITIVITY (does ignore_rows=0.2 leave residual burn-in?)")
    print("=" * 72)
    STATS.append("BURN-IN SENSITIVITY")
    for key in ["y3_mnu", "y3_kmin", "roman41_mnu"]:
        print(f"\n{key}")
        STATS.append(f"\n{key}")
        for ig in [0.2, 0.3, 0.5]:
            s = load(CH[key], settings={'ignore_rows': ig, 'contours': [0.68]})
            out = []
            for p in ['omegam', 'S8']:
                st = s.getMargeStats().parWithName(p)
                out.append(f"{p}={st.mean:.4f} "
                           f"+{st.limits[0].upper - st.mean:.4f} "
                           f"-{st.mean - st.limits[0].lower:.4f}")
            line = f"  ignore_rows={ig}: " + " | ".join(out) + f" | N={len(s.weights)}"
            print(line)
            STATS.append(line)
    STATS.append("")


def mnu_1d():
    keys = ['roman41_mnu', 'roman60_mnu', 'y1_mnu', 'y3_mnu']
    labels = ['ROMAN_Y1_41', 'ROMAN_Y1_60', 'DES_Y1', 'DES_Y3']
    samples = [load(CH[k]) for k in keys]
    ls = ['-', '-.', ':', '--']
    g = plots.get_subplot_plotter(subplot_size=2.4, width_inch=2.8)
    g.settings.figure_legend_frame = False
    g.plot_1d(samples, 'mnu', colors=COLORS[:4], ls=ls, lws=[2.0] * 4)
    ax = g.get_axes()
    ax.axvline(0.06, color='k', lw=0.8, ls=':', alpha=0.6)
    ax.set_xlabel(r'$\sum m_\nu\,[\mathrm{eV}]$')
    handles = [Line2D([0], [0], color=c, ls=l, lw=2.0)
               for c, l in zip(COLORS[:4], ls)]
    g.fig.legend(handles, labels, loc='lower center',
                 bbox_to_anchor=(0.55, 0.90), ncol=2, frameon=False, fontsize=9)
    g.export(str(FIG / 'fig5_mnu_marginals_1D.jpg'), dpi=300)
    print(f"saved {FIG / 'fig5_mnu_marginals_1D.jpg'}")


if __name__ == '__main__':
    burnin_diagnostic()

    # (1) Roman: fixed vs marginalized mnu
    compare_chains_single(
        filepaths=[CH['roman41'], CH['roman41_mnu'], CH['roman60'], CH['roman60_mnu']],
        labels=['ROMAN_41 fix $m_\\nu$', 'ROMAN_41 free $m_\\nu$',
                'ROMAN_60 fix $m_\\nu$', 'ROMAN_60 free $m_\\nu$'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8', 'mnu'],
        savepath=str(FIG / 'fig1_roman_fix_vs_free_mnu.jpg'), stats_sink=STATS)

    # (2) DES: fixed vs marginalized mnu
    compare_chains_single(
        filepaths=[CH['y1'], CH['y1_mnu'], CH['y3'], CH['y3_mnu']],
        labels=['DES_Y1 fix $m_\\nu$', 'DES_Y1 free $m_\\nu$',
                'DES_Y3 fix $m_\\nu$', 'DES_Y3 free $m_\\nu$'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8', 'mnu'],
        savepath=str(FIG / 'fig2_des_fix_vs_free_mnu.jpg'), stats_sink=STATS)

    # (3) our COCOA mnu chains vs the published chains (correctly paired)
    compare_chains_single(
        filepaths=[CH['y1_mnu'], CH['y1_pub']],
        labels=['DES_Y1_COCOA free $m_\\nu$', 'DES_Y1 published'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8'],
        savepath=str(FIG / 'fig3a_cocoa_vs_published_Y1.jpg'), stats_sink=STATS)

    compare_chains_single(
        filepaths=[CH['y3_mnu'], CH['y3_pub']],
        labels=['DES_Y3_COCOA free $m_\\nu$', 'DES_Y3 published (incl. SR)'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8'],
        savepath=str(FIG / 'fig3b_cocoa_vs_published_Y3.jpg'), stats_sink=STATS)

    # (4) kmin test: no-extrap vs production, against the published chain
    compare_chains_single(
        filepaths=[CH['y1_kmin'], CH['y1_mnu'], CH['y1_pub']],
        labels=['DES_Y1 no extrap_kmin', 'DES_Y1 extrap_kmin', 'DES_Y1 published'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8'],
        savepath=str(FIG / 'fig4a_kmin_check_Y1.jpg'), stats_sink=STATS)

    compare_chains_single(
        filepaths=[CH['y3_kmin'], CH['y3_mnu'], CH['y3_pub']],
        labels=['DES_Y3 no extrap_kmin', 'DES_Y3 extrap_kmin',
                'DES_Y3 published (incl. SR)'],
        params=DELTA, print_stats=True, params_stats=['omegam', 'S8'],
        savepath=str(FIG / 'fig4b_kmin_check_Y3.jpg'), stats_sink=STATS)

    # (5) mnu marginals
    mnu_1d()

    with open(FIG / 'stats.txt', 'w') as f:
        f.write('\n'.join(STATS) + '\n')
    print(f"saved {FIG / 'stats.txt'}")
