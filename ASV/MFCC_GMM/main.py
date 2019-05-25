'''
    Audio replay detection challenge for automatic speaker verification anti-spoofing

    ===========================================================
    implemention of the system for replay detection based on
    MFCC + GMM
    ===========================================================
'''

import librosa as lrs
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
from joblib import Parallel, delayed
import soundfile as sf
import multiprocessing
from sklearn import metrics
from python_speech_features import mfcc
from python_speech_features import delta

# compute number of cpus
cpu_cnt = multiprocessing.cpu_count()

# set paths to the wav files and protocols 
pathToTrainData = '../ASVspoof2017_V2/ASVspoof2017_V2_train'
pathToDevData = '../ASVspoof2017_V2/ASVspoof2017_V2_dev'
pathTotrainProtocol = '../ASVspoof2017_V2/protocol_V2/ASVspoof2017_V2_train.trn.txt'
pathTodevProtocol = '../ASVspoof2017_V2/protocol_V2/ASVspoof2017_V2_dev.trl.txt'

# read train protocol and get filelist and labels
filelist = []
labels = []
with open(pathTotrainProtocol, 'r') as f:
    for line in f:
        splits = line.strip().split(' ')
        filelist.append(splits[0])
        labels.append(splits[1])

# get indices of genuine and spoof files
genuineIdx = [x for x in range(len(labels)) if labels[x] == 'genuine']
spoofIdx = [x for x in range(len(labels)) if labels[x] == 'spoof']

# Feature extraction for training data

'''
    @param wavFilePath: the path of the .wav file
    return: mfcc feature of the given audio file with 39 dimentions
        13 mfcc_features + 13 delta_mfcc_features + 13 delta2delta_mfcc_features
'''
def extract_mfcc_feat(wavFilePath):
    x, fs = sf.read(wavFilePath)
    feat_mfcc = mfcc(x, fs, winlen=0.025, winstep=0.01, numcep=13, winfunc=np.hamming)
    print(feat_mfcc.shape)
    exit()
    delta_mfcc = delta(feat_mfcc, 2)
    delta2delta_mfcc = delta(delta_mfcc, 2)
    feat = np.concatenate((feat_mfcc, delta_mfcc, delta2delta_mfcc), axis=1)
    return feat

## extract feature for GENUINE training data and store in numpy array
print('Extracting feature for GENUINE training data...')
# loop in parallel
genuineFeatureArr = Parallel(n_jobs=cpu_cnt)(delayed(extract_mfcc_feat)(pathToTrainData + '/' +
    filelist[genuineIdx[i]]) for i in range(len(genuineIdx)))
genuineFeatureFrames = []
for m in genuineFeatureArr:
    for i in range(m.shape[0]):
        genuineFeatureFrames.append(m[i])
genuineFeatureFrames = np.mat(genuineFeatureFrames)
#print(genuineFeatureFrames.shape)
print('Done')

exit()

## extract feature for SPOOF training data and store in numpy array
print('Extracting feature for SPOOF training data...')
#loop in parallel
spoofFeatureArr = Parallel(n_jobs=cpu_cnt)(delayed(extract_mfcc_feat)(pathToTrainData + '/' + 
    filelist[spoofIdx[i]]) for i in range(len(spoofIdx)))
spoofFeatureFrames = []
for m in spoofFeatureArr:
    for i in range(m.shape[0]):
        spoofFeatureFrames.append(m[i])
spoofFeatureFrames = np.mat(spoofFeatureFrames)
#print(spoofFeatureFrames.shape)
print('Done')

# GMM training

## train GMM for GENUINE data
print('Training GMM for GENUINE...')
genuineGMM = GMM(n_components=64,  max_iter=100, verbose=2, verbose_interval=1)
genuineGMM.fit(genuineFeatureFrames)
print('Done')

## train GMM for SPOOF data
print('Training GMM for SPOOF...')
spoofGMM = GMM(n_components=64,  max_iter=100, verbose=2, verbose_interval=1)
spoofGMM.fit(spoofFeatureFrames)
print('Done')



# Feature extraction and scoring of development data

#read dev protocol and get filelist and labels
filelist = []
labels = []
with open(pathTodevProtocol, 'r') as f:
    for line in f:
        splits = line.strip().split(' ')
        filelist.append(splits[0])
        labels.append(splits[1])

# process each dev trial: feature extraction and scoring
scores = np.zeros(len(filelist))
print('Computing scores for dev trials...')
'''
    @param filePath: the path of .wav file
    return: it's score computing from GMM 
'''
def extract_feat_and_score(filePath):
    mfcc = extract_mfcc_feat(filePath)
    # score computation
    llk_genuine = np.mean(genuineGMM.score(mfcc))
    llk_spoof = np.mean(spoofGMM.score(mfcc))
    return llk_genuine - llk_spoof

scores = Parallel(n_jobs=cpu_cnt)(delayed(extract_feat_and_score)(pathToDevData + '/' + 
    filelist[i]) for i in range(len(filelist)))
print('Done')

# compute performance 
fpr, tpr, threshold = metrics.roc_curve(labels, scores, pos_label='genuine')
fnr = 1 - tpr
eer = fpr[np.nanargmin(np.absolute((fnr - fpr)))] * 100
print('ERR is %.2f' % eer)