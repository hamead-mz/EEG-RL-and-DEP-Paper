from pandas import read_csv, read_excel
from numpy import load
import numpy as np

from configuration.local import directories

def load_experiment_data():

    BehavioralData = read_excel(directories['beh_dir_file'])

    Performance_data = read_csv(directories['perform_data_dir'])

    return BehavioralData, Performance_data

def available_subjects():

    SOI = load(directories['ListOfAvailableSubjects'])

    return SOI

def grp_index_gen(group = 'CTRL'):

    BehavioralData, _ = load_experiment_data()
    SOI = available_subjects()

    Sub_G = [[], []] # first element is CTRL Group Members and the Second one the DEP Group
    for i, sub_i in enumerate(SOI[0]):

        if BehavioralData['BDI'][sub_i] < 10:

            Sub_G[0].append([i, sub_i])

        else:

            Sub_G[1].append([i, sub_i])

    if group == 'DEP':

        return Sub_G[1]
    
    else:

        return Sub_G[0]
    
def time_vector_generator_with_overlap(st = -0.4, ft = 0.8, Fs = 500, win_length = 100, overlap_ratio = 0.96, TimePos = 'end'):

    from numpy import ceil, linspace

    assert TimePos in ['middle', 'start', 'end']

    if TimePos == 'middle':

        StartTime = st + win_length / (Fs * 2)
        EndTime = ft - win_length / (Fs * 2)

    elif TimePos == 'start':

        StartTime = st
        EndTime = ft - win_length / (Fs)

    elif TimePos == 'end':

        StartTime = st + win_length / (Fs)
        EndTime = ft

    NumberOfTimeSamples = int(ceil(((ft - st) * Fs - win_length + 1) / (win_length * (1 - overlap_ratio))))

    TimeVector = linspace(StartTime, EndTime, NumberOfTimeSamples)

    return TimeVector 

def nasty_subject_indicator():

    BehavioralData, _ = load_experiment_data()
    SOI = available_subjects()

    Sub_G = [[], []] # first element is CTRL Group Members and the Second one the DEP Group
    for i, sub_i in enumerate(SOI[0]):

        if BehavioralData['BDI'][sub_i] < 10:

            Sub_G[0].append([i, sub_i])

        else:

            Sub_G[1].append([i, sub_i])

    return SOI, Sub_G

def early_late_trial_stager(data_length, upper_limit = 25, lower_limit = 10, marginal_percentage = 0.1):

    selected_bunch = np.clip(np.int32(np.round(data_length * marginal_percentage)), lower_limit, upper_limit)

    return np.array([np.linspace(start = 0, stop = selected_bunch - 1, num = selected_bunch), np.linspace(start = data_length - selected_bunch, stop = data_length - 1, num = selected_bunch)], dtype = int)