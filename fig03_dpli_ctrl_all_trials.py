import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_1samp

from src.graph_plotting import population_to_edge, network_graph
from src.plotting import significance_label_generator
from data2plot.dpli_data import extract_dpli_data

from configuration.local import directories
from configuration.general import names
from src.multiple_tests import correct_pvalues
from configuration.arg_mng import CORRECTION

from src.io import handle_figure

def generate_figure(data, config):

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    scalp_image = plt.imread(directories['scalp_img_directories'])

    fig = plt.figure(figsize = config['figure_args']['figsize'], layout = config['figure_args']['layout'], dpi = config['figure_args']['dpi'])

    subfigs = fig.subfigures(1, 2, width_ratios = config['subfigure_args']['width_ratios'], wspace = config['subfigure_args']['wspace'])

    WeMat = np.array([[population_to_edge(np.array(dPLI)[:, TimeSample, :, :], correction=CORRECTION) for TimeSample in range(11)] for dPLI in data['all_dplis']])
    # WeMat = np.array([[population_to_edge(dPLI[IND_2D, TimeSample, :, :]) for TimeSample in range(11)] for dPLI in data['AlldPLIs']])

    ####### Box Plots Section ########

    axs1 = subfigs[0].subplots(3, 1, sharex = True)
    # fig, axs1 = plt.subplots(3, 1, dpi = 1200, figsize = (3, 4.5), layout = 'constrained', sharex = True)

    for Pi in range(3):
        
        ax = axs1[Pi]
        dPLI = np.array(data['all_dplis'][Pi])
        Data2Box = [dPLI[:, config['graph_args']['times'][0], 0, 1],
                    dPLI[:, config['graph_args']['times'][1], 0, 1],
                    dPLI[:, config['graph_args']['times'][2], 0, 1],
                    dPLI[:, config['graph_args']['times'][0], 1, 3],
                    dPLI[:, config['graph_args']['times'][1], 1, 3],
                    dPLI[:, config['graph_args']['times'][2], 1, 3]]
        bxp = ax.boxplot(Data2Box, patch_artist=True,
                boxprops=dict(facecolor = config['boxplot_args']['box_colors'][Pi], edgecolor='black'),
                medianprops=dict(color='orange'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'))

        # for di, data_ in enumerate(Data2Box):

        #     pV = ttest_1samp(data_, 0.5).pvalue
        #     ax.text(di + 1, 1.1, significance_label_generator(pV * (2 * config['boxplot_args']['correct_it'] + 1)), ha = 'center', va = 'center', fontsize = 7)
        #     ax.plot([di + 1 - config['boxplot_args']['ddi'], di + 1 + config['boxplot_args']['ddi']], [1.01, 1.01], lw = 0.5, color = 'k')

        # ---------- Multiple-comparison correction ----------

        raw_p = [
            ttest_1samp(data_, 0.5).pvalue
            for data_ in Data2Box
        ]

        corrected_p = correct_pvalues(
            raw_p,
            method=CORRECTION,
        )

        for di, pV in enumerate(corrected_p):

            ax.text(
                di + 1,
                1.1,
                significance_label_generator(pV),
                ha='center',
                va='center',
                fontsize=7
            )

            ax.plot(
                [
                    di + 1 - config['boxplot_args']['ddi'],
                    di + 1 + config['boxplot_args']['ddi']
                ],
                [1.01, 1.01],
                lw=0.5,
                color='k'
            )
        
        ax.set_ylim([-0.05, 1.2])

        for direction in names['directions']:

                ax.spines[direction].set_linewidth(0.3)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_ylabel(config['event_labels'][Pi])

    # labels = 
    axs1[2].set_xticks([1, 2, 3, 4, 5, 6], config['time_labels'], rotation = 20, fontsize = 6)

    axs1[2].text(2, -0.85, "FPz - Fz", ha = 'center', va = 'center', fontsize = 8)
    axs1[2].text(5, -0.85, "Fz - Pz", ha = 'center', va = 'center', fontsize = 8)

    ######## Graphs' Section ########

    axs2 = subfigs[1].subplots(3, 3)

    alpha = 0.4

    for Pi in range(3):
        
        for tii, time_inv in enumerate(config['graph_args']['times']):

            ax = axs2[Pi, tii]
        
            BrainNetwork = network_graph(WeMat[Pi].transpose(1, 2, 0) * config['graph_args']['imp'])
            BrainNetwork.SetCoords(config['graph_args']['coords'])
            BrainNetwork.SetLabels(config['graph_args']['node_labels'])
            BrainNetwork.SetTimes(np.arange(11))
            BrainNetwork.DrawStaticGraph(0.05, window = time_inv, ax = ax, show_labels = True, 
                                         xlims = [-1.5, 1.5], ylims = [-1, 1.1], DirectionBias = 0, 
                                         Colors = config['graph_args']['color_events'][Pi], 
                                         FigConstants = config['graph_args']['n_fig_consts'])
            ax.imshow(scalp_image, extent = [-1.2, 1.2, -1, 1], alpha = alpha)

    axs2[2, 0].text(0, -1.7, '0 - 0.2 s', ha = 'center', va = 'center')
    axs2[2, 1].text(0, -1.7, '0.1 - 0.3 s', ha = 'center', va = 'center')
    axs2[2, 2].text(0, -1.7, '0.2 - 0.4 s', ha = 'center', va = 'center')

    panel_axes = [axs1[0], axs2[0, 0]]

    for ax, lab in zip(panel_axes, list('AB')):
        ax.text(-0.05, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))


    fig.supylabel('dPLI')
    # plt.show()

    return fig

def build_config(dpi = 1200):

    class Color_Pun:

        Edge = 'C2'
        Marker_Face = 'gray'
        Marker_Edge = 'k'

    class Color_Rew:

        Edge = 'C1'
        Marker_Face = 'gray'
        Marker_Edge = 'k'

    class Color_Stim:

        Edge = 'C0'
        Marker_Face = 'gray'
        Marker_Edge = 'k'

    class NFigConsts:

        StaticGraph = {

            'figsize': (5, 5),
            'edgesize': 4,
            'labelsize': 6,
            'ArrowHeadWidth': 0.2,
            'ArrowBodyWidth': 0.04,
            'ArrowHeadLength': 0.2,

        }

        MarkerAlpha = 1
        XBias = [-0.05, 0, 0, 0.1]
        YBias = [0.3, 0.2, 0.2, 0.2]

    Color_Events = [Color_Stim, Color_Rew, Color_Pun]
     
    boxplot_args = {
         
         'ddi': 0.2,
         'correct_it': 0,
         'box_colors': ['C0', 'C1', 'C2'],
    }

    event_labels = ['Stimulus', 'Reward', 'Punishment']

    figure_args = {
         
         'figsize': (5.4, 3),
         'layout': 'constrained', 
         'dpi': dpi
    }

    subfigure_args = {
         
         'width_ratios': [16, 20],
         'wspace': 0.01,
    }

    graph_args = {
         
         'imp': 1,
         'times': [4, 5, 6],
         'coords': [[-1.2, 0.1], [-0.6, 0.85], [0.2, 0.95], [1, 0.5]],
         'node_labels': ['Fpz', 'Fz', 'Cz', 'Pz'],
         'n_fig_consts': NFigConsts,
         'color_events': Color_Events,
    }

    time_labels = ['0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s', '0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s']

    config = {

         'graph_args': graph_args,
         'subfigure_args': subfigure_args,
         'figure_args': figure_args,
         'event_labels': event_labels,
         'boxplot_args': boxplot_args,
         'time_labels': time_labels
    }

    return config

def build_data(group):

    all_dplis = extract_dpli_data(group)
     
    data = {
         
         'all_dplis': all_dplis,

    }

    return data

def build_figure(dpi = 1200, SHOW = False, SAVE = True, FORMAT = 'png', MAIN_DIR = ''):

    data = build_data(group = 'CTRL')
    config = build_config(dpi = 1200)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'main-03')

    # if SAVE:

    #     fig.savefig(MAIN_DIR + r"figures\main\fig03_dpli_ctrl_all_trials." + FORMAT, dpi=1000)

    # if SHOW:

    #     plt.show()

if __name__ == '__main__':

    build_figure()