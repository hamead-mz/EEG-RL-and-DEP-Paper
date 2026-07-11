import numpy as np
from scipy.stats import zscore

from src.io import clusteredEEG_loader
from src.utils import grp_index_gen

def extract_all_event_erp_data(channel = 3,
                               events = ['Stim', 'Neg', 'Pos'],
                               start_time = -0.4,
                               end_time = 0.8,
                               Fs = 500,
                               event_keys = ['stimulus', 'reward', 'punishment'],
                               grp_lbls = ['CTRL', 'DEP']):

    data_ERP = {}
    
    start_sample = int((start_time + 0.4) * Fs)
    end_sample = int((end_time + 0.4) * Fs)    

    all_subjects = [grp_index_gen(group = grp_) for grp_ in grp_lbls]

    for ei, event in enumerate(events):

        raw_data, data_lengths = clusteredEEG_loader(event)

        data_ERP[event_keys[ei]] = {}

        for grp_num, grp_lbl in enumerate(grp_lbls):

            data_ERP[event_keys[ei]][grp_lbl] = np.array([np.mean(zscore(raw_data[sub_i[0]][:data_lengths[sub_i[0]], channel, start_sample : end_sample], axis = -1), axis = 0) for sub_i in all_subjects[grp_num]])
        
    return data_ERP