names = {

    'electrodes': ['FPz', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T7', 'C3', 'Cz', 'C4', 'T8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'Oz'],
    'freq_bands': ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'LowBeta', 'HighBeta', 'LowGamma', 'MidGamma', 'HighGamma', 'All'],
    'events': ['All', 'Neg', 'Pos', 'Stim', 'Actions', 'TestStim', 'TestActions', 'AB_FB', 'CD_FB', 'EF_FB'],
    'directions': ['top', 'bottom', 'right', 'left'],

}

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