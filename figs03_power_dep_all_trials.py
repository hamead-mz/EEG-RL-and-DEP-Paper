# from matplotlib import pyplot as plt
# from matplotlib.gridspec import GridSpec
# import numpy as np
# from scipy.stats import ttest_rel

# from src.plotting import confidence_bounds_generator, plot_scalp_topography, load_coords, wavelet_freqs_ret, movmean, p_value_text_gen
# from data2plot.power_data import extract_broad_power_data, extract_theta_power_data, topomap_gen
# from src.utils import grp_index_gen
# from src.io import handle_figure
# from configuration.general import names

# ## Power in Section A is Normalized!
# ## I mean, it is not comparable with the Section B

# def generate_figure(data, config, fs = 500, start_time = -0.4, end_time = 0.8, tAB = (300, 450), k = 100):

#     plt.style.use('seaborn-v0_8-paper')
#     plt.rcParams["font.family"] = "Times New Roman"
    
#     fig = plt.figure(figsize = config['figure']['figsize'], layout = config['figure']['layout'], dpi = config['figure']['dpi'])

#     gs = GridSpec(1, 9, figure = fig)

#     subfigs = []
#     # subfigs = fig.subfigures(1, 2)

#     subfigs.append(fig.add_subfigure(gs[:3]))
#     subfigs.append(fig.add_subfigure(gs[3:]))

#     gs1 = GridSpec(3, 1, figure = subfigs[0])

#     axs1 = []

#     axs1.append(subfigs[0].add_subplot(gs1[0]))
#     axs1.append(subfigs[0].add_subplot(gs1[1]))
#     axs1.append(subfigs[0].add_subplot(gs1[2]))

#     gs2 = GridSpec(3, 6, figure = subfigs[1])

#     axs2 = []

#     axs2.append(subfigs[1].add_subplot(gs2[:2, 1:6]))
#     axs2.append(subfigs[1].add_subplot(gs2[2, :2]))
#     axs2.append(subfigs[1].add_subplot(gs2[2, 2:4]))
#     axs2.append(subfigs[1].add_subplot(gs2[2, 4:]))

#     mean_heatmaps = [np.mean(data['broad_band_power'][i], axis = 0) for i in range(3)]

#     vmax = np.max(mean_heatmaps)
#     vmin = np.min(mean_heatmaps)

#     T, F = np.meshgrid(np.linspace(start_time + k / fs, end_time, data['broad_band_power'][2].shape[2]), data['freqs'])

#     ax = axs1[0]
#     p_stim = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[0]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)

#     ax = axs1[1]
#     p_pos = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[1]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)

#     ax = axs1[2]
#     p_neg = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[2]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)
#     ax.set_xlabel('time (s)')

#     cbar_ax = subfigs[1].add_axes([0.0, 0.5, 0.035, 0.4], zorder = 1)


#     cbar = fig.colorbar(p_stim, ax = [axs1[0], axs1[1], axs1[2]], cax = cbar_ax, orientation = 'vertical')
#     cbar.set_label('')

#     cbar.ax.text(0.75, -0.05, "Power (dB)", 
#                 ha='center', va='top', transform=cbar.ax.transAxes, fontsize = 8)

#     for i, ax in enumerate(axs1):

#         ax.axvline(0, color = 'k', ls = '--')
#         ax.axhline(3, color = 'k', ls = ':')
#         ax.axhline(8, color = 'k', ls = ':')
#         ax.set_title(['Stimulus', 'Reward', 'Punishment'][i])

#     subfigs[0].supylabel('Frequency (Hz)')
#     # Frontal Theta Power

    
#     ax = axs2[0]

#     time2P = np.linspace(start_time + k  / fs, end_time, fs + 1)

#     # Data_ = [theta_band_power[0], theta_band_power[2], theta_band_power[1]]

#     for Di, Data_Event in enumerate(data['theta_band_power']):

#         # Data2Plot = movmean(Data_Event ** 2, k)
#         Data2Plot = np.array([movmean(data ** 2, k) for data in np.array(Data_Event)])

#         y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = config['plot']['CoLe'])
#         ax.plot(time2P, np.mean(Data2Plot, axis = 0), label = data['event_labels'][Di])
#         ax.fill_between(time2P, y_L, y_U, alpha = config['plot']['alpha'])

#     ax.autoscale(axis = 'x', enable = True, tight = True)
#     ax.legend(frameon = False)
#     ax.set_title("Theta Band Power (~4-8 Hz)")
#     ax.set_xlabel('time (s)')

#     tA, tB = tAB

#     ax.axvline(0, color = 'k', lw = 0.8, ls = '-.')
#     ax.axvline(0.2, ls = ':', lw = 0.6, color = 'r')
#     ax.axvline(0.5, ls = ':', lw = 0.6, color = 'r')

#     ax.axvspan(0.2, 0.5, color = 'gray', alpha = 0.15)

#     # ax.set_ylim([0, 5.5])

#     ax.set_ylabel('Power ($\mu^2$)')

#     DataP = np.mean(np.array(data['theta_band_power'][1])[:, tA : tB], axis = 1)
#     DataR = np.mean(np.array(data['theta_band_power'][2])[:, tA : tB], axis = 1)

#     p = ttest_rel(DataP, DataR).pvalue

#     p_value_text = p_value_text_gen(p)

#     props = dict(boxstyle='round', facecolor='wheat', alpha = 0.5)
#     ax.text(0.55, 0.9, p_value_text, ha = 'center', va = 'center', bbox = props, transform=ax.transAxes)

#     for axs in [axs1, axs2]:

#         for ax in axs:

#             for direction in names['directions']:

#                 ax.spines[direction].set_linewidth(0.3)

#     panel_axes = [axs1[0], axs2[0], axs2[1]]

#     for ax, lab in zip(panel_axes, list('ABC')):
#         ax.text(-0.025, 1.15, lab,
#                 transform=ax.transAxes, ha='right', va='top',
#                 fontsize=12, fontweight='bold',
#                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))

#     # Power Topographies

#     topomap = data['topomap']
#     topomap_args = config['topomap']

#     vmin = np.min(topomap)
#     vmax = np.max(topomap)

#     ax = axs2[1]

#     colorbar = False

#     plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[0, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
#     ax.set_title('Stimulus')

#     ax = axs2[2]

#     colorbar = False

#     plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[1, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
#     ax.set_title('Reward')

#     ax = axs2[3]

#     colorbar = True

#     _, _, cbar = plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[2, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
#     ax.set_title('Punishment')

#     return fig

# def build_config(dpi):

#     figure_args = {

#         'layout': 'constrained',
#         'figsize': (9 * 0.9, 5 * 0.9),
#         'dpi': dpi,
#     }

#     plot_args = {

#         'CoLe': 1,
#         'alpha': 0.4,

#     }

#     _, WCh_Coords = load_coords()
#     Coords = np.array([WCh_Coords[:, 1], WCh_Coords[:, 0]]).T

#     topomap_args = {

#         'cmap': 'viridis',
#         'HR': 85,
#         'NG': 200,
#         'Coords': Coords,
#         'Normer': 1,
#         'n_levels': 10,
#     }

#     config = {
#         "figure": figure_args,
#         "plot": plot_args,
#         "topomap": topomap_args,
#     }

#     print('Configurations built ...')

#     return config

# def build_data(group = 'CTRL'):

#     grp_idx = grp_index_gen(group = group)

#     start_time = -0.4
#     end_time = 0.8
#     broad_band_power = extract_broad_power_data(Sub_G = grp_idx, start_time = start_time, end_time = end_time)

#     print('Broad band data built ...')

#     # end_time = 1.0
#     theta_band_power = extract_theta_power_data(Sub_G = grp_idx, start_time = start_time, end_time = end_time)

#     print('Theta band data built ...')

#     topomap = topomap_gen(SubG = grp_idx)

#     print('Topography map built ...')
    
#     freqs = wavelet_freqs_ret()

#     data = {
#     "broad_band_power": broad_band_power,
#     "theta_band_power": theta_band_power,
#     "topomap": topomap,
#     "freqs": freqs,
#     "event_labels": ['Stimulus', 'Reward', 'Punishment'],
#     }

#     return data

# def build_figure():

#     from configuration.arg_mng import dpi

#     config = build_config(dpi = dpi)
#     data = build_data(group = 'DEP')

#     fig = generate_figure(data, config)

#     handle_figure(fig, fig_name = 'supp-03')

#     # fig.savefig(r"figures\supplementary\figs03_power_dep_all_trials.png", dpi=1000)

#     # plt.show()

# if __name__ == '__main__':

#     build_figure()

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import ttest_rel

from src.plotting import confidence_bounds_generator, plot_scalp_topography, load_coords, wavelet_freqs_ret, movmean, p_value_text_gen
from data2plot.power_data import extract_broad_power_data, extract_theta_power_data, topomap_gen
from src.utils import available_subjects, load_experiment_data, grp_index_gen
from src.io import handle_figure


from src.multiple_tests import correct_pvalues
from configuration.arg_mng import CORRECTION

from configuration.general import names, time_params

## Power in Section A is Normalized!
## I mean, it is not comparable with the Section B

def generate_figure(data, config, fs = 500, 
                    start_time = time_params['start_time'],
                      end_time = time_params['end_time'], 
                      tAB = (300, 450), 
                      k = 100):

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"
    
    fig = plt.figure(figsize = config['figure']['figsize'], layout = config['figure']['layout'], dpi = config['figure']['dpi'])

    gs = GridSpec(1, 9, figure = fig)

    subfigs = []
    # subfigs = fig.subfigures(1, 2)

    subfigs.append(fig.add_subfigure(gs[:3]))
    subfigs.append(fig.add_subfigure(gs[3:]))

    gs1 = GridSpec(3, 1, figure = subfigs[0])

    axs1 = []

    axs1.append(subfigs[0].add_subplot(gs1[0]))
    axs1.append(subfigs[0].add_subplot(gs1[1]))
    axs1.append(subfigs[0].add_subplot(gs1[2]))

    gs2 = GridSpec(3, 6, figure = subfigs[1])

    axs2 = []

    axs2.append(subfigs[1].add_subplot(gs2[:2, 1:6]))
    axs2.append(subfigs[1].add_subplot(gs2[2, :2]))
    axs2.append(subfigs[1].add_subplot(gs2[2, 2:4]))
    axs2.append(subfigs[1].add_subplot(gs2[2, 4:]))

    mean_heatmaps = [np.mean(data['broad_band_power'][i], axis = 0) for i in range(3)]

    vmax = np.max(mean_heatmaps)
    vmin = np.min(mean_heatmaps)

    T, F = np.meshgrid(np.linspace(start_time + k / fs, end_time, data['broad_band_power'][2].shape[2]), data['freqs'])

    ax = axs1[0]
    p_stim = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[0]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)

    ax = axs1[1]
    p_pos = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[1]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)

    ax = axs1[2]
    p_neg = ax.pcolormesh(T, F, np.flipud(mean_heatmaps[2]), shading='auto', cmap = 'seismic', vmin = vmin, vmax = vmax)
    ax.set_xlabel('time (s)')

    cbar_ax = subfigs[1].add_axes([0.0, 0.5, 0.035, 0.4], zorder = 1)


    cbar = fig.colorbar(p_stim, ax = [axs1[0], axs1[1], axs1[2]], cax = cbar_ax, orientation = 'vertical')
    cbar.set_label('')

    cbar.ax.text(0.75, -0.05, "Power (dB)", 
                ha='center', va='top', transform=cbar.ax.transAxes, fontsize = 8)

    for i, ax in enumerate(axs1):

        ax.axvline(0, color = 'k', ls = '--')
        ax.axhline(3, color = 'k', ls = ':')
        ax.axhline(8, color = 'k', ls = ':')
        ax.set_title(['Stimulus', 'Reward', 'Punishment'][i])

    subfigs[0].supylabel('Frequency (Hz)')
    # Frontal Theta Power

    
    ax = axs2[0]

    time2P = np.linspace(start_time + k  / fs, end_time, fs + 1)

    # Data_ = [theta_band_power[0], theta_band_power[2], theta_band_power[1]]

    for Di, Data_Event in enumerate(data['theta_band_power']):

        # Data2Plot = movmean(Data_Event ** 2, k)
        Data2Plot = np.array([movmean(data ** 2, k) for data in np.array(Data_Event)])

        y_L, y_U = confidence_bounds_generator(Data2Plot, confidence_level = config['plot']['CoLe'])
        ax.plot(time2P, np.mean(Data2Plot, axis = 0), label = data['event_labels'][Di])
        ax.fill_between(time2P, y_L, y_U, alpha = config['plot']['alpha'])

    ax.autoscale(axis = 'x', enable = True, tight = True)
    ax.legend(frameon = False)
    ax.set_title("Theta Band Power (~4-8 Hz)")
    ax.set_xlabel('time (s)')

    tA, tB = tAB

    ax.axvline(0, color = 'k', lw = 0.8, ls = '-.')
    ax.axvline(0.2, ls = ':', lw = 0.6, color = 'r')
    ax.axvline(0.5, ls = ':', lw = 0.6, color = 'r')

    ax.axvspan(0.2, 0.5, color = 'gray', alpha = 0.15)

    # ax.set_ylim([0, 5.5])

    ax.set_ylabel('Power ($\mu^2$)')

    # DataP = np.mean(np.array(data['theta_band_power'][1])[:, tA : tB], axis = 1)
    # DataR = np.mean(np.array(data['theta_band_power'][2])[:, tA : tB], axis = 1)

    # p = ttest_rel(DataP, DataR).pvalue

    # p_value_text = p_value_text_gen(p)

    DataS = np.mean(np.array(data['theta_band_power'][0])[:, tA:tB], axis=1)
    DataP = np.mean(np.array(data['theta_band_power'][1])[:, tA:tB], axis=1)
    DataR = np.mean(np.array(data['theta_band_power'][2])[:, tA:tB], axis=1)

    raw_p = [
        ttest_rel(DataS, DataP).pvalue,
        ttest_rel(DataS, DataR).pvalue,
        ttest_rel(DataP, DataR).pvalue,
    ]

    corrected_p = correct_pvalues(
        raw_p,
        method=CORRECTION,
    )

    # Reward vs Punishment
    p_value_text = p_value_text_gen(max(corrected_p))

    props = dict(boxstyle='round', facecolor='wheat', alpha = 0.5)
    ax.text(0.55, 0.9, p_value_text, ha = 'center', va = 'center', bbox = props, transform=ax.transAxes)

    for axs in [axs1, axs2]:

        for ax in axs:

            for direction in names['directions']:

                ax.spines[direction].set_linewidth(0.3)

    panel_axes = [axs1[0], axs2[0], axs2[1]]

    for ax, lab in zip(panel_axes, list('ABC')):
        ax.text(-0.025, 1.15, lab,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2))

    # Power Topographies

    topomap = data['topomap']
    topomap_args = config['topomap']

    vmin = np.min(topomap)
    vmax = np.max(topomap)

    ax = axs2[1]

    colorbar = False

    plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[0, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
    ax.set_title('Stimulus')

    ax = axs2[2]

    colorbar = False

    plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[1, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
    ax.set_title('Reward')

    ax = axs2[3]

    colorbar = True

    _, _, cbar = plot_scalp_topography(ax = ax, ch_xy = topomap_args['Coords'] / topomap_args['Normer'], ch_values = topomap[2, :], show_colorbar = colorbar, head_radius = topomap_args['HR'], ears = True, n_grid = topomap_args['NG'], vmin = vmin, vmax = vmax, cmap = topomap_args['cmap'], n_levels = topomap_args['n_levels'], contour = True)
    ax.set_title('Punishment')

    return fig

def build_config(dpi = 1200):

    figure_args = {

        'layout': 'constrained',
        'figsize': (9 * 0.9, 5 * 0.9),
        'dpi': dpi,
    }

    plot_args = {

        'CoLe': 1,
        'alpha': 0.4,

    }

    _, WCh_Coords = load_coords()
    Coords = np.array([WCh_Coords[:, 1], WCh_Coords[:, 0]]).T

    topomap_args = {

        'cmap': 'viridis',
        'HR': 85,
        'NG': 200,
        'Coords': Coords,
        'Normer': 1,
        'n_levels': 10,
    }

    config = {
        "figure": figure_args,
        "plot": plot_args,
        "topomap": topomap_args,
    }

    print('Configurations built ...')

    return config

def build_data(group = 'DEP'):

    grp_idx = grp_index_gen(group = group)

    start_time = time_params['start_time']
    end_time = time_params['end_time']
    broad_band_power = extract_broad_power_data(Sub_G = grp_idx, start_time = start_time, end_time = end_time)

    print('Broad band data built ...')

    # end_time = 1.0
    theta_band_power = extract_theta_power_data(Sub_G = grp_idx, start_time = start_time, end_time = end_time)

    print('Theta band data built ...')

    topomap = topomap_gen(SubG = grp_idx)

    print('Topography map built ...')
    
    freqs = wavelet_freqs_ret()

    data = {
    "broad_band_power": broad_band_power,
    "theta_band_power": theta_band_power,
    "topomap": topomap,
    "freqs": freqs,
    "event_labels": ['Stimulus', 'Reward', 'Punishment'],
    }

    return data

def build_figure():

    from configuration.arg_mng import dpi

    config = build_config(dpi = dpi)
    data = build_data()

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'supp-03')

    # if SAVE:

    #     fig.savefig(MAIN_DIR + r"figures\main\fig02_power_ctrl_all_trials." + FORMAT, dpi=dpi)

    # if SHOW:

    #     plt.show()

def test_topomap_gen():

    BehavioralData, _ = load_experiment_data()
    SOI = available_subjects()

    Sub_G = [[], []] # first element is CTRL Group Members and the Second one the DEP Group

    for i, sub_i in enumerate(SOI[0]):

        if BehavioralData['BDI'][sub_i] < 10:

            Sub_G[0].append([i, sub_i])

        else:

            Sub_G[1].append([i, sub_i])

    topomap = topomap_gen(SubG = Sub_G[1])

    print('Topography map built ...')

    return True

if __name__ == '__main__':

    build_figure()