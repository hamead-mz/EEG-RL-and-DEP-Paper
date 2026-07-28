# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.stats import ttest_1samp

# from src.plotting import significance_label_generator
# from data2plot.dpli_data import extract_dpli_data
# from src.io import handle_figure
# from configuration.general import names

# def generate_figure(data, config):

#     plt.style.use('seaborn-v0_8-paper')
#     plt.rcParams["font.family"] = "Times New Roman"

#     ####### Box Plots Section ########

#     fig, axs1 = plt.subplots(3, 4,
#                              figsize = config['figure_args']['figsize'], 
#                              layout = config['figure_args']['layout'], 
#                              dpi = config['figure_args']['dpi'],
#                              sharex = True, 
#                              sharey = True)

#     ConnsPairs = [[0, 2],
#                 [0, 3],
#                 [1, 2],
#                 [2, 3]]

#     for CPi, ConnPair in enumerate(ConnsPairs):

#         for Pi in range(3):

#             ax = axs1[Pi, CPi]
#             dPLI = np.array(data['all_dplis'][Pi])
#             Data2Box = [dPLI[:, 4, ConnPair[0], ConnPair[1]],
#                         dPLI[:, 5, ConnPair[0], ConnPair[1]],
#                         dPLI[:, 6, ConnPair[0], ConnPair[1]]]

#             bxp = ax.boxplot(Data2Box, patch_artist=True,
#                     boxprops=dict(facecolor = config['boxplot_args']['box_colors'][Pi], edgecolor='black'),
#                     medianprops=dict(color='orange'),
#                     whiskerprops=dict(color='black'),
#                     capprops=dict(color='black'))

#             for di, data_ in enumerate(Data2Box):

#                 pV = ttest_1samp(data_, 0.5).pvalue
#                 ax.text(di + 1, 1.1, significance_label_generator(pV * (2 * config['boxplot_args']['correct_it'] + 1)), ha = 'center', va = 'center', fontsize = 7)
#                 ax.plot([di + 1 - config['boxplot_args']['ddi'], di + 1 + config['boxplot_args']['ddi']], [1.01, 1.01], lw = 0.5, color = 'k')

#             ax.set_ylim([-0.05, 1.2])

#             for direction in names['directions']:

#                     ax.spines[direction].set_linewidth(0.3)

#             ax.spines['top'].set_visible(False)
#             ax.spines['right'].set_visible(False)

#             if CPi == 0:
                
#                 ax.set_ylabel(config['event_labels'][Pi])

#             if Pi == 2:
                
#                 ax.set_xticks([1, 2, 3], config['time_labels'][:3], rotation = 20, fontsize = 6)

#     axs1[0, 0].set_title("FPz - Cz", fontsize = 8)
#     axs1[0, 1].set_title("FPz - Pz", fontsize = 8)
#     axs1[0, 2].set_title("Fz - Cz", fontsize = 8)
#     axs1[0, 3].set_title("Cz - Pz", fontsize = 8)


#     fig.supylabel('dPLI')
#     fig.supxlabel('Time Windows')

#     return fig

# def build_config(dpi):
     
#     boxplot_args = {
         
#          'ddi': 0.2,
#          'correct_it': 0,
#          'box_colors': ['C0', 'C1', 'C2'],
#     }

#     event_labels = ['Stimulus', 'Reward', 'Punishment']

#     figure_args = {
         
#          'figsize': (6, 3),
#          'layout': 'constrained', 
#          'dpi': dpi
#     }

#     time_labels = ['0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s', '0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s']

#     config = {

#         #  'subfigure_args': subfigure_args,
#          'figure_args': figure_args,
#          'event_labels': event_labels,
#          'boxplot_args': boxplot_args,
#          'time_labels': time_labels
#     }

#     return config

# def build_data(group):

#     all_dplis = extract_dpli_data(group)
     
#     data = {
         
#          'all_dplis': all_dplis,

#     }

#     return data

# def build_figure():

#     from configuration.arg_mng import dpi

#     data = build_data(group = 'DEP')
#     config = build_config(dpi)

#     fig = generate_figure(data, config)

#     handle_figure(fig, fig_name = 'supp-06')

#     # fig.savefig(r"figures\supplementary\figs06_dpli_dep_all_trials_put_top_down_bottom_up.png", dpi=1200)

#     # plt.show()

# if __name__ == '__main__':

#     build_figure()

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_1samp

from src.plotting import significance_label_generator
from data2plot.dpli_data import extract_dpli_data
from src.io import handle_figure
from configuration.general import names

from src.multiple_tests import correct_pvalues
from configuration.arg_mng import CORRECTION

def generate_figure(data, config):

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    ####### Box Plots Section ########

    fig, axs1 = plt.subplots(3, 4,
                             figsize = config['figure_args']['figsize'], 
                             layout = config['figure_args']['layout'], 
                             dpi = config['figure_args']['dpi'],
                             sharex = True, 
                             sharey = True)

    ConnsPairs = [[0, 2],
                [0, 3],
                [1, 2],
                [2, 3]]

    for CPi, ConnPair in enumerate(ConnsPairs):

        # for Pi in range(3):

        #     ax = axs1[Pi, CPi]
        #     dPLI = np.array(data['all_dplis'][Pi])
        #     Data2Box = [dPLI[:, 4, ConnPair[0], ConnPair[1]],
        #                 dPLI[:, 5, ConnPair[0], ConnPair[1]],
        #                 dPLI[:, 6, ConnPair[0], ConnPair[1]]]

        #     bxp = ax.boxplot(Data2Box, patch_artist=True,
        #             boxprops=dict(facecolor = config['boxplot_args']['box_colors'][Pi], edgecolor='black'),
        #             medianprops=dict(color='orange'),
        #             whiskerprops=dict(color='black'),
        #             capprops=dict(color='black'))

        #     for di, data_ in enumerate(Data2Box):

        #         pV = ttest_1samp(data_, 0.5).pvalue
        #         ax.text(di + 1, 1.1, significance_label_generator(pV * (2 * config['boxplot_args']['correct_it'] + 1)), ha = 'center', va = 'center', fontsize = 7)
        #         ax.plot([di + 1 - config['boxplot_args']['ddi'], di + 1 + config['boxplot_args']['ddi']], [1.01, 1.01], lw = 0.5, color = 'k')

        #     ax.set_ylim([-0.05, 1.2])

        #     for direction in names['directions']:

        #             ax.spines[direction].set_linewidth(0.3)

        #     ax.spines['top'].set_visible(False)
        #     ax.spines['right'].set_visible(False)

        #     if CPi == 0:
                
        #         ax.set_ylabel(config['event_labels'][Pi])

        #     if Pi == 2:
                
        #         ax.set_xticks([1, 2, 3], config['time_labels'][:3], rotation = 20, fontsize = 6)

        # ----------------------------------------------------------
        # Collect p-values for this connection (3 events × 3 windows)
        # ----------------------------------------------------------

        tests = []

        for Pi in range(3):

            dPLI = np.array(data['all_dplis'][Pi])

            Data2Box = [
                dPLI[:, 4, ConnPair[0], ConnPair[1]],
                dPLI[:, 5, ConnPair[0], ConnPair[1]],
                dPLI[:, 6, ConnPair[0], ConnPair[1]],
            ]

            for di, data_ in enumerate(Data2Box):

                p = ttest_1samp(data_, 0.5).pvalue
                tests.append((Pi, di, p))

        raw_p = [x[2] for x in tests]

        corrected_p = correct_pvalues(
            raw_p,
            method=CORRECTION,
        )

        p_dict = {
            (Pi, di): p
            for (Pi, di, _), p in zip(tests, corrected_p)
        }

        # ----------------------------------------------------------
        # Plot
        # ----------------------------------------------------------

        for Pi in range(3):

            ax = axs1[Pi, CPi]

            dPLI = np.array(data['all_dplis'][Pi])

            Data2Box = [
                dPLI[:, 4, ConnPair[0], ConnPair[1]],
                dPLI[:, 5, ConnPair[0], ConnPair[1]],
                dPLI[:, 6, ConnPair[0], ConnPair[1]],
            ]

            bxp = ax.boxplot(
                Data2Box,
                patch_artist=True,
                boxprops=dict(
                    facecolor=config['boxplot_args']['box_colors'][Pi],
                    edgecolor='black'
                ),
                medianprops=dict(color='orange'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black')
            )

            for di in range(3):

                pV = p_dict[(Pi, di)]

                ax.text(
                    di + 1,
                    1.1,
                    significance_label_generator(pV),
                    ha='center',
                    va='center',
                    fontsize=7,
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

            if CPi == 0:
                ax.set_ylabel(config['event_labels'][Pi])

            if Pi == 2:
                ax.set_xticks(
                    [1, 2, 3],
                    config['time_labels'][:3],
                    rotation=20,
                    fontsize=6,
                )

    axs1[0, 0].set_title("FPz - Cz", fontsize = 8)
    axs1[0, 1].set_title("FPz - Pz", fontsize = 8)
    axs1[0, 2].set_title("Fz - Cz", fontsize = 8)
    axs1[0, 3].set_title("Cz - Pz", fontsize = 8)


    fig.supylabel('dPLI')
    fig.supxlabel('Time Windows')

    return fig

def build_config(dpi):
     
    boxplot_args = {
         
         'ddi': 0.2,
         'correct_it': 0,
         'box_colors': ['C0', 'C1', 'C2'],
    }

    event_labels = ['Stimulus', 'Reward', 'Punishment']

    figure_args = {
         
         'figsize': (6, 3),
         'layout': 'constrained', 
         'dpi': dpi
    }

    time_labels = ['0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s', '0 - 0.2 s', '0.1 - 0.3 s', '0.2 - 0.4 s']

    config = {

        #  'subfigure_args': subfigure_args,
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

def build_figure():

    from configuration.arg_mng import dpi

    data = build_data(group = 'DEP')
    config = build_config(dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'supp-06')

    # fig.savefig(r"figures\supplementary\figs05_dpli_ctrl_all_trials_put_top_down_bottom_up.png", dpi=1200)

    # plt.show()

if __name__ == '__main__':

    build_figure()