import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sps

from configuration.general import names
from data2plot.dpli_data import extract_dplis_across_all_trials_both_reward_punishment
from data2plot.behavioral_data import load_learning_rate_gain_loss_ctrl_dep

from src.io import handle_figure

from src.multiple_tests import correct_pvalues
from configuration.arg_mng import CORRECTION

# def generate_figure(data, config,
#                     alpha_dots = 0.6,
#                     times_io = [4, 5],
#                     origin = np.array([0.1, 0.9])):
    
#     plt.style.use('seaborn-v0_8-paper')
#     plt.rcParams["font.family"] = "Times New Roman"

#     fig, axs = plt.subplots(2, 2, 
#                             layout = config['figure_args']['layout'], 
#                             dpi = config['figure_args']['dpi'], 
#                             figsize = config['figure_args']['figsize'], 
#                             sharex=True, sharey = True)

#     for time_idx, time_io in enumerate(times_io):

#         for event_num, event_key in enumerate(['reward', 'punishment']):

#             ax = axs[event_num, time_idx]

#             X_all = [np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1], 
#                      np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1], 
#                      np.concatenate((np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1], np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1]))]
            
#             Y_all = [data['learning_rate']['CTRL'][event_key],
#                      data['learning_rate']['DEP'][event_key],
#                      np.concatenate((data['learning_rate']['CTRL'][event_key], data['learning_rate']['DEP'][event_key]))]
            
#             p_grp = []
            
#             for data_idx, (X, Y) in enumerate(zip(X_all, Y_all)):

#                 linreg = sps.linregress(X, Y)
#                 p_grp.append(np.round(sps.pearsonr(X, Y).pvalue, 3))

#                 label___  = config['group_labels'][data_idx] + f'(p = {p_grp[-1]})'
#                 ax.plot(origin, linreg.slope * origin + linreg.intercept, 
#                         color = config['dot_colors'][data_idx], label = label___,
#                         ls = config['line_styles'][data_idx])
                
#                 if data_idx < 2:

#                     ax.scatter(X, Y, s = 10, alpha = alpha_dots, label = config['group_labels'][data_idx], color = config['group_colors'][data_idx])

#             if time_idx == 1 and event_key == 'punishment':

#                 ax.legend()

#             else:

#                 ax.text(x = config['text_locs'][event_num][time_idx][0], 
#                         y = config['text_locs'][event_num][time_idx][1],
#                         s = f'CTRL: p = {p_grp[0]}\nDEP: p = {p_grp[1]}\nAll: p = {p_grp[2]}', 
#                             va = 'center', fontsize = 8)

#     ### Texts on title and right

#     axs[0, 0].set_ylabel('Gain - Locked to Reward')
#     axs[1, 0].set_ylabel('Loss - Locked to Punishment')

#     axs[0, 0].set_title('0 - 0.2 s')
#     axs[0, 1].set_title('0.1 - 0.3 s')

#     for ax_ in axs:

#         for ax in ax_:

#             for direction in names['directions']:

#                 ax.spines[direction].set_linewidth(0.3)

#                 if direction in ['right', 'top']:

#                     ax.spines[direction].set_visible(False)

#     fig.supylabel('Learning Rate')
#     fig.supxlabel('dPLI')
    
#     return fig

def generate_figure(data, config,
                    alpha_dots=0.6,
                    times_io=[4, 5],
                    origin=np.array([0.1, 0.9])):

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams["font.family"] = "Times New Roman"

    fig, axs = plt.subplots(
        2, 2,
        layout=config['figure_args']['layout'],
        dpi=config['figure_args']['dpi'],
        figsize=config['figure_args']['figsize'],
        sharex=True,
        sharey=True
    )

    # ----------------------------------------------------------
    # Multiple-comparison correction
    # ----------------------------------------------------------

    tests = []

    for time_idx, time_io in enumerate(times_io):

        for event_num, event_key in enumerate(['reward', 'punishment']):

            X_all = [
                np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1],
                np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1],
                np.concatenate((
                    np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1],
                    np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1]
                ))
            ]

            Y_all = [
                data['learning_rate']['CTRL'][event_key],
                data['learning_rate']['DEP'][event_key],
                np.concatenate((
                    data['learning_rate']['CTRL'][event_key],
                    data['learning_rate']['DEP'][event_key]
                ))
            ]

            for group_idx, (X, Y) in enumerate(zip(X_all, Y_all)):

                p = sps.pearsonr(X, Y).pvalue
                tests.append((time_idx, event_num, group_idx, p))

    raw_p = [x[3] for x in tests]

    corrected_p = correct_pvalues(
        raw_p,
        method=CORRECTION,
    )

    p_dict = {
        (time_idx, event_num, group_idx): p
        for (time_idx, event_num, group_idx, _), p
        in zip(tests, corrected_p)
    }

    # ----------------------------------------------------------
    # Plot
    # ----------------------------------------------------------

    for time_idx, time_io in enumerate(times_io):

        for event_num, event_key in enumerate(['reward', 'punishment']):

            ax = axs[event_num, time_idx]

            X_all = [
                np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1],
                np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1],
                np.concatenate((
                    np.array(data['dpli']['CTRL'][event_key])[:, time_io, 0, 1],
                    np.array(data['dpli']['DEP'][event_key])[:, time_io, 0, 1]
                ))
            ]

            Y_all = [
                data['learning_rate']['CTRL'][event_key],
                data['learning_rate']['DEP'][event_key],
                np.concatenate((
                    data['learning_rate']['CTRL'][event_key],
                    data['learning_rate']['DEP'][event_key]
                ))
            ]

            p_grp = []

            for data_idx, (X, Y) in enumerate(zip(X_all, Y_all)):

                linreg = sps.linregress(X, Y)

                p = p_dict[(time_idx, event_num, data_idx)]
                p_grp.append(np.round(p, 3))

                label___ = config['group_labels'][data_idx] + f' (p = {p_grp[-1]:.3f})'

                ax.plot(
                    origin,
                    linreg.slope * origin + linreg.intercept,
                    color=config['dot_colors'][data_idx],
                    label=label___,
                    ls=config['line_styles'][data_idx]
                )

                if data_idx < 2:

                    ax.scatter(
                        X,
                        Y,
                        s=10,
                        alpha=alpha_dots,
                        color=config['group_colors'][data_idx]
                    )

            if time_idx == 1 and event_key == 'punishment':

                ax.legend()

            else:

                ax.text(
                    x=config['text_locs'][event_num][time_idx][0],
                    y=config['text_locs'][event_num][time_idx][1],
                    s=(
                        f'CTRL: p = {p_grp[0]:.3f}\n'
                        f'DEP: p = {p_grp[1]:.3f}\n'
                        f'All: p = {p_grp[2]:.3f}'
                    ),
                    va='center',
                    fontsize=8
                )

    ### Texts on title and right

    axs[0, 0].set_ylabel('Gain - Locked to Reward')
    axs[1, 0].set_ylabel('Loss - Locked to Punishment')

    axs[0, 0].set_title('0 - 0.2 s')
    axs[0, 1].set_title('0.1 - 0.3 s')

    for ax_ in axs:

        for ax in ax_:

            for direction in names['directions']:

                ax.spines[direction].set_linewidth(0.3)

                if direction in ['right', 'top']:

                    ax.spines[direction].set_visible(False)

    fig.supylabel('Learning Rate')
    fig.supxlabel('dPLI')

    return fig

def build_data():

    data = {

         'dpli': extract_dplis_across_all_trials_both_reward_punishment(),
         'learning_rate': load_learning_rate_gain_loss_ctrl_dep()
    }
      
    return data

def build_config(dpi = 1200):

    figure_args = {

        'figsize': (6, 4),
         'layout': 'constrained', 
         'dpi': dpi
    }
     
    config = {
         
        'figure_args': figure_args,
        'group_labels': ['CTRL', 'DEP', 'All'],
        'dot_colors': ['C0', 'C1', 'k'],
        'line_styles': ['--', '--', '-'],
        'text_locs': [[(0.4, 0.15), (0, 0.15)],
                     [(0.0, 0.85), (0, 0.8)]],
        'group_colors': ['C0', 'C1']

    }
      
    return config

def build_figure():

    from configuration.arg_mng import dpi
     
    data = build_data()
    config = build_config(dpi = dpi)

    fig = generate_figure(data, config)

    handle_figure(fig, fig_name = 'supp-09')

if __name__ == '__main__':

    build_figure()