import sys
import getopt
from sklearn.mixture import GaussianMixture as GMM
from utils import result_io
from utils import feature_extractor
import numpy as np
import os

rootPath = os.path.split(os.path.abspath(sys.argv[0]))[0]

threshold = 3.957640

def extract_feat_and_score(genuineGMM, spoofGMM, fileName):
    cimfcc = feature_extractor.extract_cimfcc_feat(fileName)
    # score computation
    llk_genuine = np.mean(genuineGMM.score(cimfcc))
    llk_spoof = np.mean(spoofGMM.score(cimfcc))
    return llk_genuine - llk_spoof


def estimate(fileName, genuineGMM, spoofGMM):
    llk = extract_feat_and_score(genuineGMM, spoofGMM, fileName)
    if llk >= threshold:
        return True
    else:
        return False


def loadGMMs():
    genuineGMM = GMM()
    spoofGMM = GMM()
    result_io.gmm_read(genuineGMM, os.path.join(rootPath, 'gmm/genuineGMM.h5'))
    result_io.gmm_read(spoofGMM, os.path.join(rootPath, 'gmm/spoofGMM.h5'))

    return genuineGMM, spoofGMM

if __name__ == '__main__':
    genuineGMM, spoofGMM = loadGMMs()

    print(estimate(sys.argv[1], genuineGMM, spoofGMM))