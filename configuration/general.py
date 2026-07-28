names = {

    'electrodes': ['FPz', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T7', 'C3', 'Cz', 'C4', 'T8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'Oz'],
    'freq_bands': ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'LowBeta', 'HighBeta', 'LowGamma', 'MidGamma', 'HighGamma', 'All'],
    'events': ['All', 'Neg', 'Pos', 'Stim', 'Actions', 'TestStim', 'TestActions', 'AB_FB', 'CD_FB', 'EF_FB'],
    'directions': ['top', 'bottom', 'right', 'left'],

}

inc_channels = [0, 3, 8, 13]

wavelet_params = {

        'wavelet': 'morl',
        'widths_param':{

            'morl': {

                '500': {

                    'All': [8, 1024],
                    'Delta': [128, 1024],
                    'Theta': [54, 128],
                    'NomTheta': [51, 80],
                    'Alpha': [32, 54],
                    'Beta': [13, 32],
                    'Gamma': [8, 14]
                },
            },

        },

        'time_lims':{

            '100': [0, 0.2],
            '200': [0, 0.4],
            '400': [-0.2, 0.6],
            '500': [-0.4, 0.6],
            '800': [-0.4, 1.2],
            'Default': 'No'

        },

        'Spectral_Res': 20
    }

time_params = {

    'start_time': -0.4,
    'end_time': 0.8
}

FIG_NAMES = {

    'main-02': 'main\\fig02_power_ctrl_all_trials',
    'main-03': 'main\\fig03_dpli_ctrl_all_trials',
    'main-04': 'main\\fig04_dpli_ctrl_vs_dep_across_all_trials',
    'main-05': 'main\\fig05_power_both_groups_early_late_trials',
    'main-06': 'main\\fig06_dpli_both_groups_early_late_trials',
  
    'supp-02': 'supplementary\\figs02_both_groups_erp_all_trials', 
    'supp-03': 'supplementary\\figs03_power_dep_all_trials', 
    'supp-04': 'supplementary\\figs04_dpli_dep_all_trials', 
    'supp-05': 'supplementary\\figs05_dpli_ctrl_all_trials_put_top_down_bottom_up', 
    'supp-06': 'supplementary\\figs06_dpli_dep_all_trials_put_top_down_bottom_up', 
    'supp-07': 'supplementary\\figs07_dpli_both_groups_early_vs_late_trials', 
    'supp-08': 'supplementary\\figs08_dpli_both_groups_early_late_trials_stimulus_onset',
    'supp-09': 'supplementary\\figs09_dpli_vs_learning_rate_correlation_all_ctrl_dep',

}