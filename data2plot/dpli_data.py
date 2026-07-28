import numpy as np
from scipy.stats import zscore
from scipy.signal import hilbert

from src.io import clusteredEEG_loader, data_directory_generator, load_data_version_by
from src.utils import grp_index_gen, nasty_subject_indicator, early_late_trial_stager
from src.spectral import wavelet_transform

from configuration.local import directories

def extract_dpli_data(group = 'CTRL'):

    dpli_data = calculate_dpli_values_across_all(group = group)

    return dpli_data

def calculate_dpli_values_across_all(group = 'CTRL', 
                          channels = [0, 3, 8, 13], 
                          events = ['Stim', 'Pos', 'Neg'], 
                          window_length = 100, 
                          overlap_ratio = 0.5,
                          start_time = -0.4,
                          end_time = 0.8,
                          Fs = 500):

    calculated_connectivity_data = []

    grp_ind = grp_index_gen(group = group)

    sp = int((start_time + 0.4) * Fs)
    fp = int((end_time + 0.4) * Fs)

    for event in events:

        Event_Conn = []

        raw_data, data_lengths = clusteredEEG_loader(event = event)
        print("The Event is " + event)

        for i, _ in grp_ind:

            print("subject " + str(i))

            dl = int(data_lengths[i])
            data = zscore(raw_data[i][:, :, sp : fp], axis = -1)
            divData = np.mean(data[:dl, :, :], axis = 0)

            t = dpli_calculation_function(divData, overlap_ratio = overlap_ratio, 
                                               window_length = window_length, Band = 'Theta', inc_channels = channels)

            Event_Conn.append(t)

        calculated_connectivity_data.append(Event_Conn)

    return calculated_connectivity_data

def dpli_calculation_function(Data: np.ndarray, window_length = 100, overlap_ratio = 0.5, **kwargs):

    # Issues:

    options = {

        'inc_channels': np.arange(Data.shape[-2]),
        'SpecDecompKernel': 'Wavelet',
        'Band': 'All',
        'PermuteBro': False,
        'Spectral_Res': 20,
    }

    options.update(kwargs)    
    
    assert type(options['inc_channels']) == list or type(options['inc_channels']) == np.ndarray, "Included Channels must be a list or np array"
    
    channels = options['inc_channels']

    
    specs = {}
    specs['FilterInKernel'] = True    
    specs['SpecDecompKernel'] = options['SpecDecompKernel']    
    specs['Band'] = options['Band']
    specs['Spectral_Res'] = options['Spectral_Res']

    assert Data.ndim == 2 or Data.ndim == 3, "Your Data must be 3 or 2 Dimensional, (Trials (optional), Channels, Time)"

    if Data.ndim == 2:

        Data = np.reshape(Data, (1, Data.shape[0], Data.shape[1]))

    
    time_length = Data.shape[-1]
    number_of_windows = int((time_length - window_length) / ((1 - overlap_ratio) * window_length)) + 1
    number_of_trials = Data.shape[0]

    PermutateBro = options['PermuteBro']

    if len(channels) > 1 and np.all([type(electrode) in [int, np.int32] for electrode in channels]):

        i_channels = channels
        j_channels = channels

    elif len(channels) == 2:

        i_channels = channels[0]
        j_channels = channels[1]

    else:

        assert False, "Invalid Channels matrix shape"

    DC_values = np.zeros((number_of_trials, number_of_windows, len(i_channels), len(j_channels)))

    for trial_i in range(number_of_trials):

        for win_step in range(number_of_windows):

            for i, channel_a in enumerate(i_channels):

                for j, channel_b in enumerate(j_channels[:i]):

                    win_stp = int((win_step) * (1 - overlap_ratio) * window_length)
                    win_enp = win_stp + window_length

                    if PermutateBro:

                        x_t = np.random.permutation(Data[trial_i, channel_a, win_stp : win_enp])
                        y_t = np.random.permutation(Data[trial_i, channel_b, win_stp : win_enp])

                    else:

                        x_t = Data[trial_i, channel_a, win_stp : win_enp]
                        y_t = Data[trial_i, channel_b, win_stp : win_enp]

                    specs['i'] = i
                    specs['j'] = j

                    win_DC_val = dPLI(x_t, y_t, specs)
                    
                    DC_values[trial_i, win_step, i, j] = win_DC_val
                    DC_values[trial_i, win_step, j, i] = 1 - win_DC_val
            
    return np.squeeze(DC_values)

def dPLI(x, y, specs):

    return_DC = False

    if 'Band' in specs.keys():

        Band = specs['Band']

    else:

        Band = 'All'

    if Band == 'All':
    
        x_b = x
        y_b = y

    else:

        x_b = wavelet_transform(x, Band = Band)[0]
        y_b = wavelet_transform(y, Band = Band)[0]

    x_a = hilbert(x_b)
    y_a = hilbert(y_b)
    
    phase_HSs = np.heaviside(np.angle(x_a) - np.angle(y_a), 0.5)
    
    if return_DC:

        return phase_HSs
    
    else:

        return np.mean(phase_HSs)
    

def extract_dpli_data_groups_across_all_both():

    confile_dir = directories['n_confile_dir'] + "\\CommonEraData"

    subjects_of_interest, subjects_by_groups = nasty_subject_indicator()

    data_groups = {}
    event_label = ['stimulus', 'reward', 'punishment']

    for ei, event_name in enumerate(['Stim', 'Pos', 'Neg']):

        DataDir = data_directory_generator(confile_dir, event_name, band = 'All-D')
        Data, _ = load_data_version_by(DataDir)
        data_groups[event_label[ei]] = [[Data[str(subjects_of_interest[1][sub_i[0]])][:, :, :, :4, :4] for sub_i in SubSub_G] for SubSub_G in subjects_by_groups]

    return data_groups

def extract_dplis_across_all_trials_both():

    from configuration.arg_mng import CHANNEL_PAIR

    dpli_data = [calculate_dpli_values_across_all(group = group, channels = CHANNEL_PAIR) for group in ['CTRL', 'DEP']]

    data_dicts = {

        'CTRL': {

            'stimulus': dpli_data[0][0],
            'reward': dpli_data[0][1],
            'punishment': dpli_data[0][2],
        },

        'DEP': {

            'stimulus': dpli_data[1][0],
            'reward': dpli_data[1][1],
            'punishment': dpli_data[1][2],
        },
    }

    return data_dicts

def extract_early_late_ctrl_dep_dpli_data(channels = (0, 1)):

    output_data = {

        'reward': {
            'CTRL': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'CTRL', events = ['Pos'])))[:, :, :, channels[0], channels[1]],
            'DEP': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'DEP', events = ['Pos'])))[:, :, :, channels[0], channels[1]],
        },

        'punishment': {
            'CTRL': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'CTRL', events = ['Neg'])))[:, :, :, channels[0], channels[1]],
            'DEP': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'DEP', events = ['Neg'])))[:, :, :, channels[0], channels[1]],
        },
    }

    return output_data

def calculate_dpli_values_early_late(group = 'CTRL', 
                          channels = None, 
                          events = ['Stim', 'Pos', 'Neg'], 
                          window_length = 100, 
                          overlap_ratio = 0.5,
                          start_time = -0.4,
                          end_time = 0.8,
                          Fs = 500):

    if channels is None:

        from configuration.arg_mng import CHANNEL_PAIR
        channels = CHANNEL_PAIR

    calculated_connectivity_data = []

    grp_ind = grp_index_gen(group = group)

    sp = int((start_time + 0.4) * Fs)
    fp = int((end_time + 0.4) * Fs)

    for event in events:

        Event_Conn = []

        raw_data, data_lengths = clusteredEEG_loader(event = event)
        print("The Event is " + event)

        for i, _ in grp_ind:

            print("subject " + str(i))

            dl = int(data_lengths[i])
            data = zscore(raw_data[i][:, :, sp : fp], axis = -1)
            divData = np.mean(data[early_late_trial_stager(dl), :, :], axis = 1)

            t = dpli_calculation_function(divData, overlap_ratio = overlap_ratio, 
                                               window_length = window_length, Band = 'Theta', inc_channels = channels)

            Event_Conn.append(t)

        calculated_connectivity_data.append(Event_Conn)

    return calculated_connectivity_data

def extract_early_late_ctrl_dep_dpli_stimulus_locked_data(channels = (0, 1)):

    output_data = {

        'stimulus': {
            'CTRL': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'CTRL', events = ['Stim'])))[:, :, :, channels[0], channels[1]],
            'DEP': np.squeeze(np.array(calculate_dpli_values_early_late(group = 'DEP', events = ['Stim'])))[:, :, :, channels[0], channels[1]],
        },
    }

    return output_data

def extract_dplis_across_all_trials_both_reward_punishment():

    from configuration.arg_mng import CHANNEL_PAIR

    dpli_data = [calculate_dpli_values_across_all(group = group, channels = CHANNEL_PAIR, events=['Pos', 'Neg']) for group in ['CTRL', 'DEP']]

    data_dicts = {

        'CTRL': {

            'reward': dpli_data[0][0],
            'punishment': dpli_data[0][1],
        },

        'DEP': {

            'reward': dpli_data[1][0],
            'punishment': dpli_data[1][1],
        },
    }

    return data_dicts