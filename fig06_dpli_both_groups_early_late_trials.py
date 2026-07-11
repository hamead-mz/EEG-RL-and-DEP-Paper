import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

from src.plotting import confidence_bounds_generator
from src.utils import time_vector_generator_with_overlap
from data2plot.dpli_data import extract_early_late_ctrl_dep_dpli_data
from configuration.general import names

from src.io import handle_figure

def generate_figure(data, config,
                    CoLe = 1,
                    alpha = 0.4,
                    ConThr = 0.03,
                    times_toP = [4, 5, 6],
                    fig2Ytexts = [0.7, 0.3, 0.7]
                    ):
    
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"  
      
    props = dict(boxstyle='round', facecolor='wheat', alpha = 1)

    fig, axs = plt.subplots(2, 2, 
                            figsize = config['figure_args']['figsize'], 
                            layout = config['figure_args']['layout'], 
                            dpi = config['figure_args']['dpi'], 
                            sharex = True, sharey = True)
    
    for event_num, event_key in enumerate(['reward', 'punishment']):
         
         for trial_stage in range(2):

            ctrl_dpli = data['dpli'][event_key]['CTRL'][:, trial_stage, :]
            dep_dpli = data['dpli'][event_key]['DEP'][:, trial_stage, :]

            ax = axs[trial_stage, event_num]

            for group_num, dpli_data in enumerate([ctrl_dpli, dep_dpli]):

                Data2Plot = dpli_data
                ax.plot(config['lor_time'], np.mean(Data2Plot, axis = 0), 
                        color = config['color_curves'][trial_stage][group_num], label = config['group_labels'][group_num])
                y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
                ax.fill_between(config['lor_time'], y_L, y_U, alpha = alpha, color = config['color_curves'][trial_stage][group_num])

            ax.autoscale(axis = 'x', tight = True)
            ax.axvline(0, ls = '--', color = 'k')
            ax.axhline(0.5, ls = ':', color = 'r')
            ax.axvline(config['lor_time'][4], color = 'r')
            ax.axvline(config['lor_time'][5], color = 'r')

            ER_ps = []

            for ti, time_i in enumerate(times_toP):

                    pValue = ttest_ind(ctrl_dpli[:, time_i], dep_dpli[:, time_i]).pvalue
                    ER_ps.append(pValue)

                    print(pValue)

                    if pValue < ConThr:
                        
                        ax.text(config['lor_time'][time_i], fig2Ytexts[ti], f'p = {np.round(pValue, 3)}', bbox = props, ha = 'center', fontsize = 9)

                        if time_i > 5:
                            
                            ax.axvline(config['lor_time'][time_i], color = 'g', ls = '--')
                            
    axs[0, 0].set_ylabel('Early Trials')
    axs[1, 0].set_ylabel('Late Trials')

    axs[0, 1].set_title('Punishment')
    axs[0, 0].set_title('Reward')

    panel_axes = [axs[0, 0], axs[1, 0], axs[0, 1], axs[1, 1]]

    for ax, lab in zip(panel_axes, list('ABCD')):
        ax.text(-0.025, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))

    fig.supylabel('dPLI - FPz Leading Fz') # Formerly "Posterior"
    fig.supxlabel('time (s)')

    for axs in axs:
        
            for ax in axs:

                    for direction in names['directions']:

                            ax.spines[direction].set_linewidth(0.3)

    return fig

def build_data():

    data = {
         'dpli': extract_early_late_ctrl_dep_dpli_data()
    }
      
    return data

def build_config(dpi = 1200):

    figure_args = {

        'figsize': (8, 4.8),
         'layout': 'constrained', 
         'dpi': dpi
    }
     
    config = {
         
        'figure_args': figure_args,
        # 'box_colors': ['C0', 'C2', 'C1', 'C3'],
        'group_labels': ['CTRL', 'DEP'],
        'stage_labels': ['Early', 'Late'],
        'event_labels': ['Reward', 'Punishment'],
        'color_curves': [['C0', 'C1'], 
                         ['C2', 'C3']],
        'lor_time': time_vector_generator_with_overlap(overlap_ratio = 0.5),

    }
      
    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'main-06')

    # fig.savefig(r"figures\main\fig06_dpli_both_groups_early_late_trials.png", dpi = dpi)

    # plt.show()

if __name__ == '__main__':

    build_figure()