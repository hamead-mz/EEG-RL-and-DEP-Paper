import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

from src.plotting import significance_label_generator
from data2plot.dpli_data import extract_early_late_ctrl_dep_dpli_data
from src.io import handle_figure

def generate_figure(data, config,
                    times = [4, 5],
                    ):
    
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"  
      
    fig, axs = plt.subplots(2, 2, sharex=True, sharey = True, 
                            dpi = config['figure_args']['dpi'],
                            layout = config['figure_args']['layout'],
                            figsize = config['figure_args']['figsize'])
    
    labels = ['CTRL - Early', 'CTRL - Late', 'DEP - Early', 'DEP - Late']

    for event_num, event_key in enumerate(['reward', 'punishment']):

        for time_idx, time_win in enumerate(times):

            ctrl_dpli = [data['dpli'][event_key]['CTRL'][:, trial_stage, time_win] for trial_stage in range(2)]
            dep_dpli = [data['dpli'][event_key]['DEP'][:, trial_stage, time_win] for trial_stage in range(2)]

            box_data = [ctrl_dpli[0], ctrl_dpli[1], dep_dpli[0], dep_dpli[1]]

            ax = axs[event_num, time_idx]

            bxp = ax.boxplot(box_data, patch_artist = True)

            for grp_idx, grp_data in enumerate([ctrl_dpli, dep_dpli]):

                ax.plot([1 + 2 * grp_idx, 2 + 2 * grp_idx], [1, 1], color = 'k')

                pValue = ttest_rel(grp_data[0], grp_data[1]).pvalue
                ax.text(1.5  + 2 * grp_idx, 1.1, significance_label_generator(pValue), ha = 'center')

            ax.set_ylim([0, 1.2])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            for patch, color in zip(bxp['boxes'], config['box_colors']):
                
                patch.set_facecolor(color)

    panel_axes = [axs[0, 0], axs[1, 0], axs[0, 1], axs[1, 1]]

    for ax, lab in zip(panel_axes, list('ABCD')):
        ax.text(-0.025, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))
        
    axs[0, 0].set_ylabel('0 - 0.2 s')
    axs[1, 0].set_ylabel('0.1 - 0.3 s')

    axs[0, 0].set_title(config['event_labels'][0])
    axs[0, 1].set_title(config['event_labels'][1])

    axs[1, 0].set_xticks([1, 2, 3, 4], labels, rotation = 45)
    axs[1, 1].set_xticks([1, 2, 3, 4], labels, rotation = 45)
        
    fig.supylabel('dPLI FPz (Leadning) and Fz')
    
    return fig

def build_data():

    data = {
         'dpli': extract_early_late_ctrl_dep_dpli_data()
    }
      
    return data

def build_config(dpi = 1200):

    figure_args = {

        'figsize': (4, 4),
         'layout': 'constrained', 
         'dpi': dpi
    }
     
    config = {
         
        'figure_args': figure_args,
        'box_colors': ['C0', 'C2', 'C1', 'C3'],
        'event_labels': ['Reward', 'Punishment'],

    }
      
    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'supp-07')

    # fig.savefig(r"figures\supplementary\figs07_dpli_both_groups_early_vs_late_trials.png", dpi = dpi)

    # plt.show()

if __name__ == '__main__':

    build_figure()