import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from scipy.stats import zscore, ttest_ind

from src.plotting import confidence_bounds_generator, wavelet_freqs_ret
from src.utils import grp_index_gen, time_vector_generator_with_overlap
from data2plot.dpli_data import extract_dplis_across_all_trials_both, extract_dpli_data_groups_across_all_both
from src.io import handle_figure
from configuration.general import names

def generate_figure(data, config, 
                    CoLe = 1, 
                    alpha = 0.4, 
                    times_toP = [4, 5], 
                    fig2Ytexts = [0.7, 0.3, 0.35], 
                    Channel2Inv = (0, 1),
                    lw_dd = 0.5):

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    fig = plt.figure(figsize = config['figure_args']['figsize'], 
                             layout = config['figure_args']['layout'], 
                             dpi = config['figure_args']['dpi'])
    
    gs = GridSpec(6, 20, figure=fig)
    Ca, Cb = Channel2Inv

    subfigs = []
    subfigs.append(fig.add_subfigure(gs[:5, :10]))   # left
    subfigs.append(fig.add_subfigure(gs[:, 10:]))    # right

    # ---------- LEFT column: share within left only ----------
    gs1 = subfigs[0].add_gridspec(3, 2)
    axL0 = subfigs[0].add_subplot(gs1[0, 0])
    axL1 = subfigs[0].add_subplot(gs1[1, 0], sharex=axL0, sharey=axL0)
    axL2 = subfigs[0].add_subplot(gs1[2, 0], sharex=axL0, sharey=axL0)
    axs1 = [axL0, axL1, axL2]


    axC0 = subfigs[0].add_subplot(gs1[0, 1], sharex=axL0, sharey=axL0)
    axC1 = subfigs[0].add_subplot(gs1[1, 1], sharex=axL0, sharey=axL0)
    axC2 = subfigs[0].add_subplot(gs1[2, 1], sharex=axL0, sharey=axL0)
    axs3 = [axC0, axC1, axC2]

    # ---------- RIGHT column: share within right only ----------
    gs2 = subfigs[1].add_gridspec(3, 1)
    axR0 = subfigs[1].add_subplot(gs2[0])
    axR1 = subfigs[1].add_subplot(gs2[1], sharex=axR0, sharey=axR0)
    axR2 = subfigs[1].add_subplot(gs2[2], sharex=axR0, sharey=axR0)
    axs2 = [axR0, axR1, axR2]

    for ax in axs1[:-1]:
        ax.tick_params(labelbottom=False)
    for ax in axs2[:-1]:
        ax.tick_params(labelbottom=False)
    for ax in axs3[:-1]:
        ax.tick_params(labelbottom=False)
    for ax in axs3:
        ax.tick_params(labelleft = False)

    for ax in axs1[1:]:
        ax.set_ylabel("")
    for ax in axs2[1:]:
        ax.set_ylabel("")

    props = dict(boxstyle='round', facecolor='wheat', alpha = 1)

    ##### Left Subfigure -> CTRL TF-dPLI

    Data2Plot = np.mean(np.array(data['data_groups']['reward'][0])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T
    T, F = np.meshgrid(data['hir_time'], data['freq_vec'])

    ax = axs3[1]
    p_pos = ax.pcolormesh(T, F, np.flipud(power), shading='auto',
                           cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])

    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(3, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)
    
    Data2Plot = np.mean(np.array(data['data_groups']['punishment'][0])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T

    ax = axs3[2]
    p_neg = ax.pcolormesh(T, F, np.flipud(power), shading='auto', 
                          cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])
    ax.set_yscale('log')
    
    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(3, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)
    
    Data2Plot = np.mean(np.array(data['data_groups']['stimulus'][0])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T

    ax = axs3[0]
    p_stim = ax.pcolormesh(T, F, np.flipud(power), shading='auto', 
                           cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])
    ax.set_yscale('log')
    
    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(4, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)

    ##### Center Subfigure -> DEP TF-dPLI

    Data2Plot = np.mean(np.array(data['data_groups']['reward'][1])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T

    ax = axs1[1]
    p_pos = ax.pcolormesh(T, F, np.flipud(power), shading='auto',
                          cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])
    ax.set_yscale('log')
    
    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(3, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)

    Data2Plot = np.mean(np.array(data['data_groups']['punishment'][1])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T

    ax = axs1[2]
    p_neg = ax.pcolormesh(T, F, np.flipud(power), shading='auto',
                          cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])
    ax.set_yscale('log')
    
    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(3, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)

    Data2Plot = np.mean(np.array(data['data_groups']['stimulus'][1])[:, :, :, :, Ca, Cb], axis = 1)
    power = np.mean(Data2Plot, axis = 0).T

    ax = axs1[0]
    p_stim = ax.pcolormesh(T, F, np.flipud(power), shading='auto',
                           cmap = config['heatmap_args']['cmap_i'], vmin = config['heatmap_args']['vmin'], vmax = config['heatmap_args']['vmax'])
    ax.set_yscale('log')

    ax.axvline(0, color = 'k', ls = '-.', lw = lw_dd)
    ax.axhline(4, color = 'k', ls = '--', lw = lw_dd)
    ax.axhline(8, color = 'k', ls = '--', lw = lw_dd)
    
    ax = axs2[0]
    ax.set_yscale('linear')
    Data2Plot = np.array(data['dplis']['CTRL']['stimulus'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C0', label = 'CTRL')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C0')

    Data2Plot = np.array(data['dplis']['DEP']['stimulus'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C1', label = 'DEP')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C1')

    ax.autoscale(axis = 'x', tight = True)
    ax.axvline(0, ls = '--', color = 'k')
    ax.axhline(0.5, ls = ':', color = 'r')
    ax.legend(frameon = False)
    ax.axvline(data['lor_time'][times_toP[0]], color = 'r')
    ax.axvline(data['lor_time'][times_toP[1]], color = 'r')

    ax = axs2[1]

    Data2Plot = np.array(data['dplis']['CTRL']['reward'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C0', label = 'CTRL')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C0')

    Data2Plot = np.array(data['dplis']['DEP']['reward'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C1', label = 'DEP')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C1')

    ax.autoscale(axis = 'x', tight = True)
    ax.axvline(0, ls = '--', color = 'k')
    ax.axhline(0.5, ls = ':', color = 'r')
    ax.axvline(data['lor_time'][times_toP[0]], color = 'r')
    ax.axvline(data['lor_time'][times_toP[1]], color = 'r')

    for ti, time_i in enumerate(times_toP):

            pValue = ttest_ind(np.array(data['dplis']['CTRL']['reward'])[:, time_i, 0, 1], np.array(data['dplis']['DEP']['reward'])[:, time_i, 0, 1]).pvalue

            print(pValue)

            if pValue < 0.1:
                
                ax.text(data['lor_time'][time_i], fig2Ytexts[ti], f'p = {np.round(pValue, 3)}', bbox = props, ha = 'center', fontsize = 9)

    ax = axs2[2]

    Data2Plot = np.array(data['dplis']['CTRL']['punishment'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C0', label = 'CTRL')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C0')

    Data2Plot = np.array(data['dplis']['DEP']['punishment'])[:, :, 0, 1]
    ax.plot(data['lor_time'], np.mean(Data2Plot, axis = 0), color = 'C1', label = 'DEP')
    y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = CoLe)
    ax.fill_between(data['lor_time'], y_L, y_U, alpha = alpha, color = 'C1')

    ax.autoscale(axis = 'x', tight = True)
    ax.axvline(0, ls = '--', color = 'k')
    ax.axhline(0.5, ls = ':', color = 'r')
    ax.axvline(data['lor_time'][times_toP[0]], color = 'r')
    ax.axvline(data['lor_time'][times_toP[1]], color = 'r')

    for ti, time_i in enumerate(times_toP):

            pValue = ttest_ind(np.array(data['dplis']['CTRL']['punishment'])[:, time_i, 0, 1], np.array(data['dplis']['DEP']['punishment'])[:, time_i, 0, 1]).pvalue

            print(pValue)

            if pValue < 0.1:
                
                ax.text(data['lor_time'][time_i], fig2Ytexts[ti], f'p = {np.round(pValue, 3)}', bbox = props, ha = 'center', fontsize = 9)


    axs2[0].set_title('Stimulus')
    axs2[1].set_title('Reward')
    axs2[2].set_title('Punishment')

    axs1[0].set_ylabel('Stimulus')
    axs1[1].set_ylabel('Reward')
    axs1[2].set_ylabel('Punishment')

    axs1[0].set_title('DEP')
    axs3[0].set_title('CTRL')

    for axs in [axs1, axs2, axs3]:

        for ax in axs:

            for direction in names['directions']:

                ax.spines[direction].set_linewidth(0.3)

    subfigs[0].supylabel('Frequency (Hz, log scale)', fontsize = 10)
    subfigs[0].supxlabel('time (s)', fontsize = 10)

    subfigs[1].supylabel('dPLI', fontsize = 10)
    subfigs[1].supxlabel('time (s)', fontsize = 10)

    fig.text(0.29, 1.03, "Broad-Band dPLI of Fpz and Fz",
            ha="center", va="center", fontsize=11)

    fig.text(0.765, 1.03, "Theta-Band dPLI of Fpz and Fz",
            ha="center", va="center", fontsize=11)

    cbar_ax = fig.add_axes([0.175, .125, 0.2, 0.02], zorder = 1)

    fig.colorbar(p_stim, ax = [axs1[0], axs1[1], axs1[2], axs3[0], axs3[1], axs3[2]], cax = cbar_ax, orientation = 'horizontal', label = 'dPLI')

    panel_axes = [axs1[0], axs2[0]]

    for ax, lab in zip(panel_axes, list('AB')):
        ax.text(-0.05, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))
        
    return fig

def build_data():
     
    data_groups = extract_dpli_data_groups_across_all_both()
    dplis = extract_dplis_across_all_trials_both()
    hir_time = time_vector_generator_with_overlap()
    lor_time = time_vector_generator_with_overlap(overlap_ratio = 0.5)
    freq_vec = wavelet_freqs_ret()

    grp_indices = {

        'CTRL': grp_index_gen('CTRL'),
        'DEP': grp_index_gen('DEP')
    }
    
    data = {
          
         'dplis': dplis,
         'data_groups': data_groups,
         'freq_vec': freq_vec,
         'hir_time': hir_time[:125], # this is an ad-hoc modification of the code ... 
         'lor_time': lor_time,
         'grp_indices': grp_indices,
    }

    return data

def build_config(dpi, SCALE = 4 / 5):

    figure_args = {

        'figsize': (80/8 * SCALE, 16/3 * SCALE),
         'layout': 'constrained', 
         'dpi': dpi
    }

    heatmap_args = {

        'cmap_i': 'PiYG',
        'vmin': 0.3,
        'vmax': 0.7,
    }
     
    config = {
        'figure_args': figure_args,
        'heatmap_args': heatmap_args,
    }

    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'main-04')

    # fig.savefig(r"figures\main\fig04_dpli_ctrl_vs_dep_across_all_trials.png", dpi=1000)

    # plt.show()

if __name__ == '__main__':
     
    build_figure()