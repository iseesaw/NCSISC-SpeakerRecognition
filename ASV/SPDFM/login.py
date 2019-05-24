import settings
import numpy as np
import sys
from utils import phomeframe
import os
from utils import doppler_feature
from utils import scoring
import math

"""
Usage: python3 login.py [username] [wavFileDir]
assume wav file dir like this:
test
|--temp
|  |--login.wav
|  |--login.lab
TextGrid
|--login.TextGrid

"""
if __name__ == '__main__':
    username = sys.argv[1]
    wavFileDir = sys.argv[2]
    files = os.listdir(wavFileDir)
    dotprefix = files[0].split('.')[0]
    refer_pf = phomeframe.PhomeFrame.read(os.path.join(settings.ENROLL_FEATURE_PATH, username+'.h5'))
    wavPrefix = os.path.split(dotprefix)[-1]
    pf = phomeframe.PhomeFrame.read_raw(os.path.join(wavFileDir, dotprefix + '.wav'), os.path.join(wavFileDir,
                                                                         os.path.join('../TextGrid',
                                                                                      wavPrefix+'.TextGrid')))
    refer_one_feats = refer_pf.get_all_phome_feature_as_one()
    normed_pf = doppler_feature.length_normalize(pf, refer_pf)
    normed_one_feats = normed_pf.get_all_phome_feature_as_one()

    means = []
    stds = []
    for idx in range(normed_one_feats.shape[0]):
        mean, std = scoring.p_c_fusion_scoring(refer_one_feats[idx], normed_one_feats[idx])
        if math.isnan(mean) or math.isnan(std):
            means.append(settings.MAX_MEAN_VALUE)
            stds.append(settings.MAX_STD_VALUE)
        else:
            means.append(mean)
            stds.append(std)

    with open(os.path.join(settings.SCORE_PATH, username+'.s'), 'r') as f:
        line = f.readline()
        splits = line.rstrip().split(' ')
        refer_mean = float(splits[0])
        refer_std = float(splits[1])

    if np.mean(means) - refer_mean - (np.mean(stds) - refer_std) >= settings.THRESHOLD:
        print(True)
    else:
        print(False)

