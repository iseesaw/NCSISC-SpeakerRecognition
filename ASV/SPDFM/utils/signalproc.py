import numpy as np
from scipy import signal
import pywt


def stftsig(sig, fs, frame_len, frame_step, winfunc=lambda x: np.ones((x,))):
    """
    get the short-time-fourier-transform result of the given signal.

    :param sig: the audio signal to frame.
    :param fs: the sampling rate of the signal
    :param frame_len: length of sampling points each frame measured in samples.
    :param frame_step: number of samples after the start of the previous frame that the next frame should begin.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied.
    :returns: a (frame_step) x (len(sig) / frame_step) nda array
    """

    f, t, Zxx = signal.stft(x=sig, fs=fs, window=winfunc, nperseg=frame_len, noverlap=frame_step)
    return f, t, Zxx


def framesig(sig, sr, frame_len, frame_step, low_freq=19800, high_freq=20200, winfunc='blackman'):
    """

    :param sig:
    :param sr:
    :param frame_len:
    :param frame_step:
    :param low_freq:
    :param high_freq:
    :param winfunc:
    :return:
    """
    f, t, Zxx = signal.stft(x=sig, fs=sr, window=winfunc, nperseg=frame_len, noverlap=frame_step)
    low_idx = np.where(f - low_freq < 0)[0][-1]
    high_idx = np.where(f - high_freq > 0)[0][0]
    return f[low_idx:high_idx], t, Zxx[low_idx:high_idx, :].T


def wavelet_denoising(sig):
    """
    do a wavelet_soft_denoising process

    :param sig:
    :return:
    """
    w = pywt.Wavelet('db4')
    coeffs = pywt.wavedec(sig, w)
    coeffs[len(coeffs)-1] *= 0
    coeffs[len(coeffs)-2] *= 0
    denoised = pywt.waverec(coeffs, w)
    return denoised


def preemphasis(sig, coeff=0.95):
    """perform preemphasis on the input signal.

    :param sig: The signal to filter.
    :param coeff: The preemphasis coefficient. 0 is no filter, default is 0.95.
    :returns: the filtered signal.
    """
    return np.append(sig[0], sig[1:]-coeff*sig[:-1])


def bin_butterworth_filtering(sig, fs, low_freq=19800, high_freq=20200):
    """
    use butterworth filter to process signal, limiting band between 19.8kHz and 20.2kHz

    :param sig: the original signal from audio file
    :param fs: the sampling rate of signal
    :param low_freq: the low cut off frequency of the butter-worth filter
    :param high_freq: the high cur off frequency of the butter-worth filter
    :return:
    """
    nyq = 0.5 * fs
    low = low_freq / nyq
    high = high_freq / nyq
    b, a = signal.butter(N=5, Wn=[low, high], btype='band')
    filtered = signal.lfilter(b, a, sig)

    return filtered

