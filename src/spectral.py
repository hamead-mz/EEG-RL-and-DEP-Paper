import numpy as np
from pywt import cwt, frequency2scale

from configuration.general import wavelet_params, names

def wavelet_transform(data: np.ndarray, Band = 'All', wavelet = 'morl', return_freqs = False, Fs = 500, spectral_res = 50, **kwargs):

    if str(data.shape[-1]) in wavelet_params['time_lims'].keys():

        TimeLims = wavelet_params['time_lims'][str(data.shape[-1])]

    else:

        TimeLims = [0, data.shape[-1] / Fs]

    if type(Band) == str:

        WiPa = wavelet_params['widths_param'][wavelet][str(Fs)][Band]

    else:

        WiPa = assign_width_params(BandRanges = Band, Fs = Fs, Spectral_Res = spectral_res)
    
    options = {

        'widths_param': WiPa,
        'time_lims': TimeLims,
        'Spectral_Res': spectral_res

    }

    options.update(kwargs)

    widths_param = options['widths_param']
    widths = np.geomspace(widths_param[0], widths_param[1], num = options['Spectral_Res'])

    time = np.linspace(options['time_lims'][0], options['time_lims'][1], data.shape[-1])

    assert data.ndim < 4 and data.ndim > 0, "Invalid data shape"

    CWTMat_Conn = []

    for _ in range(3 - data.ndim):

        data = np.reshape(data, (1,) + data.shape)

    [Trials, Channels, Length] = data.shape

    for Channel_Num in range(Channels):

        CWTMat = np.zeros((len(widths), Length))

        for i in range(Trials):

            cwtmatr, freqs = cwt(data[i, Channel_Num, :], widths, wavelet, sampling_period = np.diff(time).mean())
            
            CWTMat = CWTMat + 1 / Trials * cwtmatr

        CWTMat_Conn.append(CWTMat)

    outputs = []
    outputs.append(np.squeeze(np.array(CWTMat_Conn)))

    if return_freqs:

        outputs.append(freqs)

    return tuple(output for output in outputs)

def assign_width_params(BandRanges, Fs, Spectral_Res, wavelet = 'morl'):

    Scales = [frequency2scale(wavelet = wavelet, freq = BandRange / Fs, precision = Spectral_Res) for BandRange in BandRanges]

    return Scales

def freq_band_extractor_1d(Data: np.ndarray, Band = 'All'): # add kwargs and method

    assert Data.ndim < 4 and Data.ndim > 0, "The data must have a time dim at least and 3 dimensions (Trial, Channel, Time) at most"
    assert type(Band) == str or type(Band) == list, "Insert true Band name"

    if type(Band) == str:

        if Band == 'All':

            Band = [Band_i for Band_i in names['freq_bands']][:5]

        else:

            Band = [Band]

    Band_Data = []

    for Band_i in Band:

        assert Band_i in names['freq_bands'], "Band Name is Not Available!"

        output = wavelet_transform(Data, Band = Band_i)

        Band_Data.append(np.mean(output[0], axis = -2))

    return np.array(Band_Data)