'''
    Audio replay detection challenge for automatic speaker verification anti-spoofing

    ===========================================================
    implemention of the system for replay detection based on
    CIMFCC + GMM
    ===========================================================
'''

import librosa as lrs
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
from joblib import Parallel, delayed
import soundfile as sf
import multiprocessing
from sklearn import metrics
from utils import feature_extractor
from utils import result_io
import matplotlib.pyplot as plt
import os

# get the root path
workdirPath = os.path.dirname(os.path.abspath(__file__))

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

## extract feature for GENUINE training data and store in numpy array
print('Extracting feature for GENUINE training data...')
# loop in parallel
genuineFeatureArr = Parallel(n_jobs=cpu_cnt)(delayed(feature_extractor.extract_cimfcc_feat)(pathToTrainData + '/' +
    filelist[genuineIdx[i]]) for i in range(len(genuineIdx)))
genuineFeatureFrames = []
for m in genuineFeatureArr:
    for i in range(m.shape[0]):
        genuineFeatureFrames.append(m[i])
genuineFeatureFrames = np.mat(genuineFeatureFrames)
print('Done')

## extract feature for SPOOF training data and store in numpy array
print('Extracting feature for SPOOF training data...')
#loop in parallel
spoofFeatureArr = Parallel(n_jobs=cpu_cnt)(delayed(feature_extractor.extract_cimfcc_feat)(pathToTrainData + '/' + 
    filelist[spoofIdx[i]]) for i in range(len(spoofIdx)))
spoofFeatureFrames = []
for m in spoofFeatureArr:
    for i in range(m.shape[0]):
        spoofFeatureFrames.append(m[i])
spoofFeatureFrames = np.mat(spoofFeatureFrames)
print('Done')


# GMM training

## train GMM for GENUINE data
print('Training GMM for GENUINE...')
genuineGMM = GMM(n_components=64,  max_iter=100, verbose=2, verbose_interval=1)
#genuineGMM.fit(genuineFeatureFrames)

## store result on disk
#result_io.gmm_write(genuineGMM, 'gmm/genuineGMM.h5')
result_io.gmm_read(genuineGMM, os.path.join(workdirPath, 'gmm/genuineGMM.h5'))
print('Done')


## train GMM for SPOOF data
print('Training GMM for SPOOF...')
spoofGMM = GMM(n_components=64,  max_iter=100, verbose=2, verbose_interval=1)
#spoofGMM.fit(spoofFeatureFrames)

## store result on disk
#result_io.gmm_write(spoofGMM, 'gmm/spoofGMM.h5')
result_io.gmm_read(spoofGMM, os.path.join(workdirPath, 'gmm/spoofGMM.h5'))
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
    cimfcc = feature_extractor.extract_cimfcc_feat(filePath)
    # score computation
    llk_genuine = np.mean(genuineGMM.score(cimfcc))
    llk_spoof = np.mean(spoofGMM.score(cimfcc))
    return llk_genuine - llk_spoof

scores = Parallel(n_jobs=cpu_cnt)(delayed(extract_feat_and_score)(pathToDevData + '/' + 
    filelist[i]) for i in range(len(filelist)))
print('Done')

# compute performance 
fpr, tpr, threshold = metrics.roc_curve(labels, scores, pos_label='genuine')
fnr = 1 - tpr
idx = np.nanargmin(np.absolute((fnr - fpr)))
eer = fpr[idx] * 100
print('ERR is %.2f%%' % eer)
print('The threshold is %f at the point of eer' % threshold[idx])

roc_auc = metrics.auc(fpr, tpr)
plt.figure()
lw = 2
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) 
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.savefig('roc.png')
