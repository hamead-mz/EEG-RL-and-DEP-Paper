import numpy as np
from scipy.stats import zscore

from src.plotting import movmean
from src.io import clusteredEEG_loader
from src.spectral import wavelet_transform, freq_band_extractor_1d
from src.utils import grp_index_gen, early_late_trial_stager

from configuration.local import directories

def extract_broad_power_data(start_time, end_time, Sub_G, k = 100, channel = 3, Fs = 500):

    sp = int((start_time + 0.4) * Fs)
    fp = int((end_time + 0.4) * Fs)

    event_band_data = []

    for event in ['Stim', 'Pos', 'Neg']:

        raw_data, data_lengths = clusteredEEG_loader(event)
        event_band_data.append([np.mean(np.array([wavelet_transform(zscore(BData), Band = 'All', Spectral_Res = 50)[0] for BData in raw_data[sub_i[0]][:data_lengths[sub_i[0]], channel, sp : fp]]), axis = 0) for sub_i in Sub_G])

        # event_band_data.append([np.mean(np.array([[wavelet_transform(zscore(DecData), Band = 'All', Spectral_Res = 50)[0] for DecData in BData] for BData in raw_data[sub_i[0]][:data_lengths[sub_i[0]], channel, sp : fp]]), axis = 1) for sub_i in Sub_G])

    event_power_data = []

    for di, data in enumerate(event_band_data):

        event_power_data.append(np.array([10 * np.log10(np.array([movmean(dataـwv ** 2, k) / np.sum(movmean(dataـwv[: 200] ** 2, k)) for dataـwv in data_sub])) for data_sub in data]))

    return event_power_data

def extract_theta_power_data(start_time, end_time, Sub_G, k = 100, channel = 3, Fs = 500):

    sp = int((start_time + 0.4) * Fs)
    fp = int((end_time + 0.4) * Fs)
    Band = 'Theta'

    Data_Band_EE = []

    for event in ['Stim', 'Pos', 'Neg']:

        raw_data, data_lengths = clusteredEEG_loader(event)
        Data_Band_EE.append([np.mean(np.mean(freq_band_extractor_1d(np.squeeze(zscore(raw_data[sub_i[0]][:data_lengths[sub_i[0]], channel, sp : fp], axis = -1)), Band = Band) ** 2, axis = 0), axis = 0) for sub_i in Sub_G])

    # Data = np.array([[movmean(data ** 2, k) for data in np.array(Data_Band_i)[:, 0, channel, :600]] for Data_Band_i in Data_Band_EE])

    return Data_Band_EE

def topomap_gen(SubG, Band = 'Theta'):

    wch_sets = []

    for dir in ['stimulus_set_dir', 'reward_set_dir', 'punishment_set_dir']:

        wch_sets.append(np.load(directories[dir], allow_pickle = True).item())

    keys = list(wch_sets[0].keys())
    grp_set = [[Set[keys[key_idx]][:20, :, :] for key_idx in np.array(SubG)[:, 0]] for Set in wch_sets]

    band_data_all_spatial = []

    for set in grp_set:

        print("A Set Started!")

        band_data_all_spatial.append([freq_band_extractor_1d(np.squeeze(zscore(set[sub_i][:, :, :], axis = -1)), Band = Band) for sub_i in range(len(grp_set))])

        print("A Set is Done!")

    all_powers_spatial = np.squeeze(np.array(band_data_all_spatial)) ** 2

    topomap = np.mean(np.mean(all_powers_spatial[:, :, :, 600 : 750], axis = -1), axis = 1)

    return topomap

def extract_early_late_ctrl_dep_power_data(start_time = -0.4, end_time = 0.8, Fs = 500, band = 'Theta', channel = 3):

    start_sample = int((start_time + 0.4) * Fs)
    end_sample = int((end_time + 0.4) * Fs)

    all_subjects = [grp_index_gen(group = grp) for grp in ['CTRL', 'DEP']]

    dict_keys = ['reward', 'punishment']
    instantaneous_power = {}

    for ei, event in enumerate(['Pos', 'Neg']):

        raw_data, data_lengths = clusteredEEG_loader(event)
        instantaneous_power[dict_keys[ei]] = [[np.array(np.mean([np.squeeze(freq_band_extractor_1d(data_, Band = band) ** 2) for data_ in np.squeeze(zscore(raw_data[sub_i[0]][early_late_trial_stager(data_lengths[sub_i[0]]), channel, start_sample : end_sample], axis = -1))], axis = 1)) for sub_i in grp_indices] for grp_indices in all_subjects]

    return instantaneous_power