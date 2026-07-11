from configuration.local import directories
from configuration.general import names
from scipy.io import loadmat
import h5py
import numpy as np

from configuration import arg_mng as args
from configuration.general import FIG_NAMES

def clusteredEEG_loader(event):

    assert type(event) == int or type(event) == str, "The 'event' must be the event name as string or event number as integer"

    if type(event) == str:

        tmp = [names['events'][i] == event for i in range(len(names['events']))]

        assert np.any(tmp), "The Event is not available"

        event_number = np.where(tmp)[0][0]

    else:

        assert event >= 0 and event < len(names['events']), "The Event is not available"
        
        event_number = event
        event = names['events'][event_number]

    eeg_file_dir = directories['eeg_file_dir'][event]

    try:

        f = loadmat(eeg_file_dir)

        raw_data = f['All_data_' + str(names['events'][event_number])]

        raw_data = raw_data.transpose(0, 2, 1, 3)

    except:

        with h5py.File(eeg_file_dir, 'r') as f:

            raw_data = f['All_data_' + str(names['events'][event_number])][:]

        raw_data = raw_data.transpose(3, 1, 2, 0)

    try:

        DataLengthsDir = directories['DataLengthsDir']

        f = loadmat(DataLengthsDir)
        data_lengths = f['data_lengths'][:, event_number]

    except:

        if event == 'Actions':

            DataLengthsDir = directories['ActionDataLengthsDir']

            f = loadmat(DataLengthsDir)
            data_lengths = f['data_lengths']

        else:

            DataLengthsDir = directories[event + 'DataLengthsDir']

            f = loadmat(DataLengthsDir)
            data_lengths = f['data_lengths']

    return raw_data, data_lengths

def data_directory_generator(confile_dir, event_name, band):

    CommonDir = confile_dir + '\\October\\AveragedTrialBased\\' + event_name + '\\ZeroAxis\\dPLI\\' + band

    return handle_directory(CommonDir)

def handle_directory(Directory):

    import os

    if not os.path.isdir(Directory):

        os.makedirs(Directory)

    return Directory

def load_data_version_by(Dir, version_number = None):

    import os
    from pandas import read_csv
    import pickle

    assert os.path.isdir(Dir), "This Data is not Available"

    VersionHistoryDF = read_csv(Dir + "\\VersionHistory.csv", index_col = 0)

    if version_number is None:

        version_number = np.array(VersionHistoryDF['VersionNumber'])[-1]

    LoadFileDir = Dir + "\\Data_Version" + str(version_number)

    with open(LoadFileDir, 'rb') as f:

        ConDataDict = pickle.load(f)

    DataSpecs = {key_SD: VersionHistoryDF[key_SD][version_number] for key_SD in VersionHistoryDF.keys()}

    return ConDataDict, DataSpecs

def handle_figure(fig, fig_name):

    if args.SAVE:

        fig.savefig(args.MAIN_DIR + r"figures\\" + FIG_NAMES[fig_name] + "." + args.FORMAT, dpi = args.dpi)

    if args.SHOW:

        from matplotlib.pyplot import show

        show()