import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ttest_rel

from src.plotting import confidence_bounds_generator, significance_label_generator
from configuration.general import names
from data2plot.erp_data import extract_all_event_erp_data

from src.io import handle_figure

def generate_figure(data, config,
                    CoLe = 1,
                    alpha = 0.4,
                    ):
    
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"  

    fig, axs = plt.subplots(4, 1, 
                            figsize = config['figure_args']['figsize'], 
                            dpi = config['figure_args']['dpi'], 
                            layout = config['figure_args']['layout'])

    ax = axs[0]

    for di, data_stim in enumerate(data['erp_data']['stimulus']):

        Data2Plot = data['erp_data']['stimulus'][data_stim]
        ax.plot(config['time_vec'], np.mean(Data2Plot, axis = 0), label = config['group_labels'][di], color = config['curve_bxp_colors'][0][di])
        y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
        ax.fill_between(config['time_vec'], y_L, y_U, alpha = alpha, color = config['curve_bxp_colors'][0][di])
        ax.axvline(0, ls = '--', lw = 0.5)
        ax.autoscale(axis = 'x', enable = True, tight = True)

    for grp_idx, grp_label in enumerate(config['group_labels']):

        ax = axs[grp_idx + 1]

        for event_num, event_key in enumerate(['reward', 'punishment']):

            Data2Plot = data['erp_data'][event_key][grp_label]
            ax.plot(config['time_vec'], np.mean(Data2Plot, axis = 0), label = config['event_labels'][event_num], color = config['curve_bxp_colors'][grp_idx + 1][event_num])
            y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
            ax.fill_between(config['time_vec'], y_L, y_U, alpha = 0.4, color = 'C2')
            ax.axvline(0, ls = '--', lw = 0.5)
            ax.autoscale(axis = 'x', enable = True, tight = True)

    for ax in axs:

        ax.legend(frameon = False)

        for direction in names['directions']:

            ax.spines[direction].set_linewidth(0.3)

    frn_time = config['frn_time']

    # frn_time = 345
    axs[1].axvline(config['time_vec'][frn_time], ls = ':', lw = 0.8, color = 'r')
    # frn_time = 340
    axs[2].axvline(config['time_vec'][frn_time], ls = ':', lw = 0.8, color = 'r')

    Data2Box = [data['erp_data']['reward']['CTRL'][:, frn_time], 
                data['erp_data']['reward']['DEP'][:, frn_time], 
                data['erp_data']['punishment']['CTRL'][:, frn_time], 
                data['erp_data']['punishment']['DEP'][:, frn_time], 
                data['erp_data']['punishment']['CTRL'][:, frn_time] - data['erp_data']['reward']['CTRL'][:, frn_time], 
                data['erp_data']['punishment']['DEP'][:, frn_time] - data['erp_data']['reward']['DEP'][:, frn_time]]
    
    labels = ['CTRL', 'DEP', 'CTRL', 'DEP', 'CTRL', 'DEP']

    ax = axs[3]
    bxp = ax.boxplot(Data2Box, patch_artist=True)
    ax.set_xticklabels(labels, rotation = 0)

    for comp_i in range(3):

        p = ttest_ind(Data2Box[2 * comp_i], Data2Box[2 * comp_i + 1]).pvalue
        ax.plot([1 + 2 * comp_i, 2 + 2 * comp_i], [1.5, 1.5], color = 'k', lw = 0.5)
        ax.text(1.5 + 2 * comp_i, 1.7, significance_label_generator(p), ha = 'center', fontsize = 8)

    ax.set_ylim([-2, 2.5])

    colors = ['C2', 'C4', 'C3', 'C5', 'C6', 'C7']
    for patch, color in zip(bxp['boxes'], colors):
        
        patch.set_facecolor(color)

    ax.text(0.15, -0.35, s = 'Punishment', transform=ax.transAxes, ha='center', va='top', fontsize = 7)
    ax.text(0.5, -0.35, s = 'Reward', transform=ax.transAxes, ha='center', va='top', fontsize = 7)
    ax.text(0.825, -0.35, s = 'Difference', transform=ax.transAxes, ha='center', va='top', fontsize = 7)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    props = dict(boxstyle='round', facecolor='wheat', alpha = 0.5)

    for idk in range(2):

        ax = axs[idk + 1]

        p = ttest_rel(Data2Box[0 + idk], Data2Box[2 + idk]).pvalue
        ax.axvspan(0.23, 0.33, color = 'gray', alpha = 0.3)

        if p < 0.001:

            ax.text(0.28, -0.5, f'p < 0.001', ha = 'center', fontsize = 8, bbox = props)

        elif p < 0.1:

            ax.text(0.28, -0.5, f'p = {np.round(p, 3)}', ha = 'center', fontsize = 8, bbox = props)

    panel_axes = [axs[0], axs[1], axs[2], axs[3]]

    for ax, lab in zip(panel_axes, list('ABCD')):
        ax.text(-0.025, 1.2, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=10, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))
        
    axs[0].set_title('Stimulus')
    axs[1].set_title('CTRL')
    axs[2].set_title('DEP')
    axs[2].set_xlabel('time (s)')

    axs[0].set_xticks([])
    axs[1].set_xticks([])

    axs[3].set_title('N2 Values and Differences')

    fig.supylabel('Amplitude ($\mu$v)', fontsize = 10)

    return fig

def build_data():

    data = {

         'erp_data': extract_all_event_erp_data()
    }
      
    return data

def build_config(dpi = 1200):

    figure_args = {

        'figsize': (3, 3 * 7 / 4),
        'layout': 'constrained', 
        'dpi': dpi
    }
     
    config = {
         
        'figure_args': figure_args,
        'box_colors': ['C0', 'C2', 'C1', 'C3'],
        'group_labels': ['CTRL', 'DEP'],
        'event_labels': ['Reward', 'Punishment'],
        'curve_bxp_colors': [['C0', 'C1'], 
                         ['C2', 'C3'],
                         ['C4', 'C5']],
        'time_vec': np.linspace(-0.4, 0.8, 600),
        'frn_time': 345,
    }
      
    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)
    handle_figure(fig, fig_name = 'supp-02')

    # fig.savefig(r"figures\supplementary\figs02_both_groups_erp_all_trials.png", dpi = dpi)

    # plt.show()

if __name__ == '__main__':

    build_figure()