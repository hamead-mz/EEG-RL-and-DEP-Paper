import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import ttest_ind, ttest_rel

from src.plotting import significance_label_generator, confidence_bounds_generator
from configuration.general import names
from data2plot.dpli_data import extract_early_late_ctrl_dep_dpli_stimulus_locked_data
from src.utils import time_vector_generator_with_overlap
from src.io import handle_figure

def generate_figure(data, config,
                    alpha = 0.4,
                    CoLe = 1,
                    times_oi = [4, 5],
                    labels = ['CTRL - Early', 'CTRL - Late', 'DEP - Early', 'DEP - Late'],
                    comp_pairs = [[[0, 1], [2, 3]],
                                  [[0, 2], [1, 3]]]):
    
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    fig = plt.figure(figsize = config['figure_args']['figsize'], #(5, 5), 
                     layout = config['figure_args']['layout'], # it was tight 
                     dpi = config['figure_args']['dpi'])

    gs = GridSpec(2, 2, figure = fig)

    axs = []

    axs.append(fig.add_subplot(gs[0, :]))
    axs.append(fig.add_subplot(gs[1, 0]))
    axs.append(fig.add_subplot(gs[1, 1]))

    ax = axs[0]

    for trial_idx in range(2):

            for grp_lbl in config['group_labels']:

                Data2Plot = data['dpli']['stimulus'][grp_lbl][:, trial_idx, :]

                label__ = grp_lbl + '-' + config['stage_labels'][trial_idx]
                ax.plot(config['lor_time'], np.mean(Data2Plot, axis = 0), label = label__, color = config['curve_bxp_colors'][trial_idx * 2])
                y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
                ax.fill_between(config['lor_time'], y_L, y_U, alpha = alpha, color = config['curve_bxp_colors'][trial_idx * 2])

    ax.autoscale(axis = 'x', tight = True)
    ax.axvline(0, ls = '--', color = 'k')
    ax.axhline(0.5, ls = ':', color = 'r')
    ax.legend(frameon = False, loc = 'upper right')
    ax.set_xlabel('time (s)')
    ax.set_title(f'Fpz (leading) - Fz Theta Band dPLI')

    for ti, time_i in enumerate(times_oi):

        ax.axvline(config['lor_time'][time_i], color = 'r')
        
    for ax in axs:

        for direction in names['directions']:

            ax.spines[direction].set_linewidth(0.3)

    ttest = [ttest_rel, ttest_ind]

    for t_idx, time_io in enumerate(times_oi):

        ax = axs[t_idx + 1]

        ctrl_dpli = data['dpli']['stimulus']['CTRL'][:, :, time_io]
        dep_dpli = data['dpli']['stimulus']['DEP'][:, :,  time_io]

        bxp_data = [ctrl_dpli[:, 0], ctrl_dpli[:, 1], dep_dpli[:, 0], dep_dpli[:, 1]]

        bxp = ax.boxplot(bxp_data, patch_artist = True)
        ax.set_xticklabels(labels, rotation = 30)

        for cmp_idx0, dual_pair in enumerate(comp_pairs):

            for cmp_idx1, sngl_pair in enumerate(dual_pair):

                ax.plot(np.array(sngl_pair) + 1, [1 + 0.15 * cmp_idx0 + 0.15 * cmp_idx0 * cmp_idx1, 1 + 0.15 * cmp_idx0 + 0.15 * cmp_idx0 * cmp_idx1], color = 'k')
                pValue = ttest[cmp_idx0](bxp_data[sngl_pair[0]], bxp_data[sngl_pair[1]]).pvalue
                ax.text(np.mean(sngl_pair) + 1, 1.05 + 0.15 * cmp_idx0 + 0.15 * cmp_idx0 * cmp_idx1, significance_label_generator(pValue), ha = 'center')
                print(pValue)

        ax.set_ylim([0, 1.375])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for patch, color in zip(bxp['boxes'], config['curve_bxp_colors']):
            
            patch.set_facecolor(color)

    axs[1].set_title('Theta-Band dPLI in\nwindow 0 - 0.2 s')
    axs[2].set_title('Theta-Band dPLI in\nwindow 0.1 - 0.3 s')

    axs[0].set_ylim([0.38, 0.68])

    axs[0].set_ylabel('dPLI')
    axs[1].set_ylabel('dPLI')

    panel_axes = [axs[0], axs[1], axs[2]]

    for ax, lab in zip(panel_axes, list('ABC')):
        ax.text(-0.025, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))
        
    return fig

def build_data():

    data = {

         'dpli': extract_early_late_ctrl_dep_dpli_stimulus_locked_data()
    }
      
    return data

def build_config(dpi):

    figure_args = {

        'figsize': (5, 5),
         'layout': 'constrained', 
         'dpi': dpi
    }
     
    config = {
         
        'figure_args': figure_args,
        'group_labels': ['CTRL', 'DEP'],
        'stage_labels': ['Early', 'Late'],
        'event_labels': ['Reward', 'Punishment'],
        'lor_time': time_vector_generator_with_overlap(overlap_ratio = 0.5),
        'curve_bxp_colors': ['C0', 'C2', 'C1', 'C3'],

    }
      
    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'supp-08')

    # fig.savefig(r"figures\supplementary\figs08_dpli_both_groups_early_late_trials_stimulus_onset.png", dpi = dpi)

    # plt.show()

if __name__ == '__main__':

    build_figure()