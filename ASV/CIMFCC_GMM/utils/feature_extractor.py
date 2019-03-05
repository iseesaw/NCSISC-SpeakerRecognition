import numpy as np
from python_speech_features import base
from python_speech_features import sigproc
from python_speech_features import delta
from scipy.fftpack import dct
import soundfile as sf

'''
    @param wavFilePath: the path of the .wav file
    return: cimfcc feature of the given audio file
        cimfcc_features + delta_cimfcc_features + delta2delta_cimfcc_features
'''
def extract_cimfcc_feat(wavFilePath):
    x, fs = sf.read(wavFilePath)
    feat = imfcc(x, fs, winlen=0.050, winstep=0.020, numcep=13, 
        nfft=1024, lowfreq=133.33, highfreq=8000, preemph=0.97, appendEnergy=False,
        winfunc=np.blackman)
    feat = cmvn(feat)
    return feat


def imfcc(signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
         nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,ceplifter=22,appendEnergy=True,
         winfunc=lambda x:np.ones((x,))):
    """Compute IMFCC features from an audio signal.

    :param signal: the audio signal from which to compute features. Should be an N*1 array
    :param samplerate: the samplerate of the signal we are working with.
    :param winlen: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
    :param winstep: the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
    :param numcep: the number of cepstrum to return, default 13
    :param nfilt: the number of filters in the filterbank, default 26.
    :param nfft: the FFT size. Default is 512.
    :param lowfreq: lowest band edge of mel filters. In Hz, default is 0.
    :param highfreq: highest band edge of mel filters. In Hz, default is samplerate/2
    :param preemph: apply preemphasis filter with preemph as coefficient. 0 is no filter. Default is 0.97.
    :param ceplifter: apply a lifter to final cepstral coefficients. 0 is no lifter. Default is 22.
    :param appendEnergy: if this is true, the zeroth cepstral coefficient is replaced with the log of the total frame energy.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied. You can use numpy window functions here e.g. winfunc=numpy.hamming
    :returns: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
    """
    highfreq= highfreq or samplerate/2
    signal = dither(signal)
    signal = sigproc.preemphasis(signal,preemph)
    frames = sigproc.framesig(signal, winlen*samplerate, winstep*samplerate, winfunc)
    pspec = sigproc.powspec(frames,nfft)
    energy = np.sum(pspec,1) # this stores the total energy in each frame
    energy = np.where(energy == 0,np.finfo(float).eps,energy) # if energy is zero, we get problems with log

    fb = get_InvertedMelfilterbanks(nfilt,nfft,samplerate,lowfreq,highfreq)
    feat = np.dot(pspec, fb.T)
    feat = np.where(feat == 0,np.finfo(float).eps,feat) # if feat is zero, we get problems with log
    feat = np.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    delta_feat = delta(feat, 2)
    delta2delta_feat = delta(delta_feat, 2)

    if appendEnergy: feat[:, 0] = np.log(energy)

    feat = np.concatenate((feat, delta_feat, delta2delta_feat), axis=1)
    return feat


def dither(signal):
    """ Add even random noise to signal to avoid 0 when do log operation

    :param signal: the audio signal from which to compute features. Should be an N*1 array
    :returns: the signal after applying even random noise
    """
    n = 2*np.random.rand(signal.shape[0]) - 1
    n *= 1 / (2**15)
    return signal + n


def hz2invertedmel(hz, lowfreq=0, highfreq=8000, samplerate=16000, nfft=512):
    """Convert a value in Hertz to inverted Mels

    :param lowfreq: lowest band edge of mel filters, default 0 Hz
    :param highfreq: highest band edge of mel filters, default samplerate/2
    :param samplerate: the samplerate of the signal we are working with
    :param nfft: the FFT size. Default is 512.
    :param hz: a value in Hz
    :returns: a value in inverted Mels
    """
    return base.hz2mel(lowfreq) + base.hz2mel(highfreq) - base.hz2mel(samplerate/2 + samplerate/nfft - hz)


def get_InvertedMelfilterbanks(nfilt=20,nfft=512,samplerate=16000,lowfreq=0,highfreq=None):
    """Compute a Inverted Mel-filterbank. The filters are stored in the rows, the columns correspond
    to fft bins. The filters are returned as an array of size nfilt * (nfft/2 + 1)

    :param nfilt: the number of filters in the filterbank, default 20.
    :param nfft: the FFT size. Default is 512.
    :param samplerate: the samplerate of the signal we are working with. Affects mel spacing.
    :param lowfreq: lowest band edge of mel filters, default 0 Hz
    :param highfreq: highest band edge of mel filters, default samplerate/2
    :returns: A numpy array of size nfilt * (nfft/2 + 1) containing filterbank. Each row holds 1 filter.
    """
    highfreq= highfreq or samplerate/2
    assert highfreq <= samplerate/2, "highfreq is greater than samplerate/2"

    # compute inverted mel filter energy center frequency
    # by first computing mel filter energy center frequency
    # and then use formula h'(m)=nfft/2 + 1 - h(nfilt+1-m)
    lowmel = base.hz2mel(lowfreq)
    highmel = base.hz2mel(highfreq)
    melpoints = np.linspace(lowmel, highmel, nfilt+2)
    melbin = np.floor((nfft+1)*base.mel2hz(melpoints)/samplerate)
    invertedmelbin = np.floor(nfft/2 + 1 - np.flip(melbin))

    fbank = np.zeros([nfilt, nfft//2+1])
    for j in range(0, nfilt):
        for i in range(int(invertedmelbin[j]), int(invertedmelbin[j+1])):
            fbank[j,i] = (i - invertedmelbin[j]) / (invertedmelbin[j+1] - invertedmelbin[j])
        for i in range(int(invertedmelbin[j+1]), int(invertedmelbin[j+2])):
            fbank[j,i] = (invertedmelbin[j+2] - i) / (invertedmelbin[j+2] - invertedmelbin[j+1])
    return fbank
    

def cmvn(feat):
    """ Compute regulation features by applying mvn
  
    :param feat: the original features
    :returns: the regulation features after applying mvn 
    """
    t = feat.T  
    mu = np.mean(t, axis=0)
    stdev = np.std(t, axis=0)
    t -= mu
    t /= stdev
    return t.T
