"""
Plotting helpers for the mnu campaign.

These are the functions from plot.ipynb, extracted verbatim so that every
script/notebook in this folder produces figures in the same style:
  - getdist settings {'ignore_rows': 0.2, 'contours': [0.68]}  (20% burn-in,
    single 68% contour)
  - delta_omegam / delta_S8 (each chain centered on its own mean) so that
    contour WIDTHS can be compared without centroid offsets confusing the eye
  - fixed axis limits [-0.2, 0.2] and the shared colour/linestyle cycle
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator

from getdist import loadMCSamples, plots, mcsamples
from utils import load_chain_parameters

# ---------------------------------------------------------------- style ----
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
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
for _k in ['axes.titlesize', 'axes.labelsize', 'legend.fontsize',
           'legend.title_fontsize', 'xtick.labelsize', 'ytick.labelsize']:
    matplotlib.rcParams[_k] = 10

columnwidth = 246 / 72.27
textwidth = 510 / 72.27

COLORS = ['#FFAF4C', '#9A6289', '#7386BE', '#959596', '#4C9987']


# ----------------------------------------------------------------- load ----
def DES_LOAD(filepath, settings):
    required_parameters = ["omegam", "sigma8"]
    parameters_y3, weights_y3 = load_chain_parameters(filepath, required_parameters)
    sample = mcsamples.MCSamples(
        samples=np.array(parameters_y3),
        weights=np.array(weights_y3),
        names=['omegam', 'sigma8'],
        labels=['$\\Omega_m$', '$\\Sigma_8$'],
        settings=settings)
    return sample


def load(filepath, settings={'ignore_rows': 0.2, 'contours': [0.68]}):
    try:
        sample = loadMCSamples(filepath, settings=settings)
    except Exception:
        print(f"Usual loading failed for {filepath}")
        try:
            sample = DES_LOAD(filepath, settings)
        except Exception:
            print(f"DES loading failed for {filepath}")
            print(f"Check your filepath or files")
            return None

    p = sample.getParams()
    s8 = p.sigma8 * (p.omegam / 0.3) ** 0.5
    try:
        sample.addDerived(s8, 'S8', label=r'S_8')
    except Exception:
        print(f"Error adding derived parameter for {filepath}")
    means = sample.getMeans()
    ix = sample.getParamNames().numberOfName('omegam')
    iy = sample.getParamNames().numberOfName('S8')
    delta_s8 = s8 - means[iy]
    delta_omegam = p.omegam - means[ix]
    try:
        sample.addDerived(delta_s8, 'delta_S8', label=r'\Delta S_8')
        sample.addDerived(delta_omegam, 'delta_omegam', label=r'\Delta \Omega_m')
    except Exception:
        True
    return sample


# ----------------------------------------------------------------- plot ----
def plot_compare(samples, labels, params, print_stats=False,
                 params_stats: list = None, savepath=None, stats_sink=None,
                 annotate=r'$\Lambda$CDM - ShearOnly'):
    g = plots.get_subplot_plotter(subplot_size=columnwidth,
                                  width_inch=columnwidth * 1.1,
                                  subplot_size_ratio=1)
    g.make_figure(nplot=1, nx=1)
    g.settings.tight_layout = False
    g.settings.title_limit = 1
    g.settings.title_limit_labels = True
    g.settings.title_limit_fontsize = 10
    g.settings.lab_fontsize = 10
    g.settings.legend_fontsize = 10
    g.settings.figure_legend_frame = False
    g.settings.axes_fontsize = 10
    g.settings.axes_labelsize = 10
    g.settings.axis_tick_max_labels = 4
    g.settings.alpha_factor_contour_lines = 3.0

    nsample = len(labels)

    g.plot_2d(
        roots=samples[:nsample],
        param_pair=params,
        legend_labels=labels,
        colors=COLORS,
        ls=['-', '-.', ':', '--', '--'],
        lws=[2.5, 2.5, 2.5, 2.5, 2.5],
        alphas=[0.3, 0.3, 0.3, 0.3, 0.3],
        filled=[True, True, True, True, True],
        lims=[-0.2, 0.2, -0.2, 0.2],
        ax=(0, 0)
    )

    ax = g.get_axes(ax=(0, 0))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.025))
    ax.xaxis.set_major_locator(MultipleLocator(0.06))
    ax.xaxis.set_minor_locator(MultipleLocator(0.03))
    ax.text(x=0.6, y=0.1, s=annotate, transform=ax.transAxes)

    linestyles = ['-', '-.', ':', (0, (3, 1, 1, 1, 1, 1)), (0, (5, 1, 2, 1, 3, 1))]
    alphas = [0.8] * 5
    filled_flags = [True] * 5

    dataset_handles = []
    for lab, c, ls, a, is_filled in zip(labels[:nsample], COLORS[:nsample],
                                        linestyles[:nsample], alphas[:nsample],
                                        filled_flags[:nsample]):
        if is_filled:
            h = Patch(facecolor=c, edgecolor=c, linestyle=ls, linewidth=2.0,
                      alpha=a, label=lab)
        else:
            h = Line2D([0], [0], color=c, linestyle=ls, linewidth=1.25,
                       alpha=a, label=lab)
        dataset_handles.append(h)

    g.legend = g.fig.legend(dataset_handles, labels, loc='lower center',
                            bbox_to_anchor=(0.55, 0.90), ncol=3,
                            frameon=False, fontsize=10)

    if print_stats:
        if params_stats is None:
            params_stats = ['omegam', 'S8']
        for isample, sample in enumerate(samples):
            for p in params_stats:
                stat = sample.getMargeStats().parWithName(p)
                if stat is None:
                    continue
                mean = stat.mean
                upper_bound = stat.limits[0].upper
                lower_bound = stat.limits[0].lower
                line = (f'{labels[isample]} {p} = {mean:.3f} '
                        f'+ {upper_bound - mean:.3f} - {mean - lower_bound:.3f}')
                print(line)
                if stats_sink is not None:
                    stats_sink.append(line)
    if stats_sink is not None:
        stats_sink.append('')

    g.extra_artists = [g.legend]
    if savepath is not None:
        g.export(savepath, dpi=300)
        print(f'saved {savepath}')


def compare_chains_single(filepaths: list, labels: list, params: list,
                          print_stats: bool = False, params_stats: list = None,
                          savepath: str = None, stats_sink=None,
                          annotate=r'$\Lambda$CDM - ShearOnly'):
    if len(filepaths) != len(labels):
        raise ValueError("filepaths and labels must have the same length")

    samples = []
    for i in range(len(filepaths)):
        samples.append(load(filepaths[i]))
        if samples[-1] is None:
            raise RuntimeError(f"Failed to load chain: {filepaths[i]}")
        pn = samples[-1].getParamNames()
        for p in pn.names:
            if p.name == 'mnu':
                p.label = r'\sum m_{\nu}'
            if p.name.lower() == 'omegan':
                p.label = r'\Omega_{\nu}'
            if p.name == 'As_1e9':
                p.label = r'10^{9} A_{\rm s}'

    plot_compare(samples, labels, params, print_stats=print_stats,
                 params_stats=params_stats, savepath=savepath,
                 stats_sink=stats_sink, annotate=annotate)
    return samples
