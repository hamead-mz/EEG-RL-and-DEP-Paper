import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import ttest_ind, ttest_rel

from src.plotting import confidence_bounds_generator, significance_label_generator, movmean
from data2plot.power_data import extract_early_late_ctrl_dep_power_data

from configuration.general import names
from src.io import handle_figure

def generate_figure(data, config, CoLe = 1, alpha = 0.4, time_shades = [250, 375],
                    time_ = np.linspace(-0.4, 0.8, 501), k = 100):
    
    # Notice a moving-average window is applied to the temporal data
    # for better visualizations, but statistical tests are 
    # run over the average of instantaneous power in 0.2-0.5 s window.

    fig = plt.figure(figsize = config['figure_args']['figsize'], layout = config['figure_args']['layout'], dpi = config['figure_args']['dpi'])
    gs = GridSpec(3, 2, figure = fig)

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    axs = []

    axs.append(fig.add_subplot(gs[0, :]))
    axs.append(fig.add_subplot(gs[1, :]))
    axs.append(fig.add_subplot(gs[2, 0]))
    axs.append(fig.add_subplot(gs[2, 1]))

    for Di, event_key in enumerate(data['power']):

        for Bi in range(2):

            for DC in range(2):

                    loaded_data_to_plot = np.array(data['power'][event_key][DC])[:, Bi, :]

                    Data2Plot = np.array([movmean(subject_data_raw, k = k) for subject_data_raw in loaded_data_to_plot])

                    label___ = config['group_labels'][DC] + ' - ' + config['stage_labels'][Bi]
                    
                    axs[Di].plot(time_, np.mean(Data2Plot, axis = 0), label = label___)
                    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
                    axs[Di].fill_between(time_, y_L, y_U, alpha = alpha)
                    axs[Di].autoscale(axis = 'x', tight = True)

        axs[Di].set_title(config['event_labels'][Di])
        axs[Di].axvline(0, color = 'k', ls = '--')

        if Di == 1:
              
            axs[Di].legend(frameon = False)

        for time_shade in time_shades:
            
            axs[Di].axvline(time_[time_shade], ls = ':', lw = 0.75)

    for axs_ in [axs]:
        
            for ax in axs_:

                    for direction in names['directions']:

                            ax.spines[direction].set_linewidth(0.3)

    labels = ['CTRL - Early', 'CTRL - Late', 'DEP - Early', 'DEP - Late']
    box_labels = ['Early', 'Late', 'Early', 'Late']

    for Di, data_event_key in enumerate(data['power']):

        data_event = data['power'][data_event_key]
         
        Early_Control = np.mean(np.array(data_event[0])[:, 0, time_shades[0] : time_shades[1]], axis = 1)
        Late_Control = np.mean(np.array(data_event[0])[:, 1, time_shades[0] : time_shades[1]], axis = 1)

        Early_Depressed = np.mean(np.array(data_event[1])[:, 0, time_shades[0] : time_shades[1]], axis = 1)
        Late_Depressed = np.mean(np.array(data_event[1])[:, 1, time_shades[0] : time_shades[1]], axis = 1)
        
        bxp = axs[2 + Di].boxplot([Early_Control, Late_Control, Early_Depressed, Late_Depressed], labels = box_labels, patch_artist=True)
        axs[2 + Di].set_xticklabels(labels, rotation = 30)
        axs[2 + Di].plot([1, 2], [25, 25], color = 'k')
        pValue = ttest_rel(Early_Control, Late_Control).pvalue
        axs[2 + Di].text(1.5, 26, significance_label_generator(pValue), ha = 'center')
        print(pValue)

        axs[2 + Di].plot([3, 4], [25, 25], color = 'k')
        pValue = ttest_rel(Early_Depressed, Late_Depressed).pvalue
        axs[2 + Di].text(3.5, 26, significance_label_generator(pValue), ha = 'center')
        print(pValue)

        axs[2 + Di].plot([1, 3], [30, 30], color = 'k')
        pValue = ttest_ind(Early_Control, Early_Depressed).pvalue
        axs[2 + Di].text(2, 31, significance_label_generator(pValue), ha = 'center')
        print(pValue)

        axs[2 + Di].plot([2, 4], [35, 35], color = 'k')
        pValue = ttest_ind(Late_Control, Late_Depressed).pvalue
        axs[2 + Di].text(3, 36, significance_label_generator(pValue), ha = 'center')
        print(pValue)

        axs[2 + Di].set_ylim([0, 40])
        axs[2 + Di].spines['top'].set_visible(False)
        axs[2 + Di].spines['right'].set_visible(False)

        for patch, color in zip(bxp['boxes'], config['box_colors']):
            
            patch.set_facecolor(color)

        axs[2 + Di].set_title(config['event_labels'][Di] + ' in\nwindow 200 - 500 ms')

        for patch, color in zip(bxp['boxes'], config['box_colors']):
            
            patch.set_facecolor(color)
            
    for i_ in range(3):
         
        axs[i_].set_ylabel('Power ($\mu^2$)')

    for i_ in range(2):
         
        axs[i_].axvspan(0.2, 0.5, color = 'gray', alpha = alpha * 0.72)

    axs[0].set_xticks([])
    
    panel_axes = [axs[0], axs[1], axs[2], axs[3]]

    for ax, lab in zip(panel_axes, list('ABCD')):
        ax.text(-0.03, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))
    
    return fig

def build_config(dpi):

    figure_args = {

        'figsize': (4, 5),
         'layout': 'constrained', 
         'dpi': dpi
    }
     
    config = {
        'figure_args': figure_args,
        'box_colors': ['C0', 'C2', 'C1', 'C3'],
        'group_labels': ['CTRL', 'DEP'],
        'stage_labels': ['Early', 'Late'],
        'event_labels': ['Reward', 'Punishment']
    }

    return config

def build_data():
     
    power_data = extract_early_late_ctrl_dep_power_data()

    return {'power': power_data}

def build_figure():

    from configuration.arg_mng import dpi
     
    config = build_config(dpi = dpi)
    data = build_data()

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'main-05')

if __name__ == '__main__':
     
    build_figure()