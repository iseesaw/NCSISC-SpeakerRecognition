import sys
import getopt
from sklearn.mixture import GaussianMixture as GMM
import result_io
import feature_extractor
import numpy as np


def extract_feat_and_score(genuineGMM, spoofGMM, fileName):
    cimfcc = feature_extractor.extract_cimfcc_feat(fileName)
    # score computation
    llk_genuine = np.mean(genuineGMM.score(cimfcc))
    llk_spoof = np.mean(spoofGMM.score(cimfcc))
    return llk_genuine - llk_spoof


def estimate(fileName, genuineGMM, spoofGMM):
    llk = extract_feat_and_score(genuineGMM, spoofGMM, fileName)
    if llk >= 0:
        return True
    else:
        return False


def loadGMMs():
    genuineGMM = GMM()
    spoofGMM = GMM()
    result_io.gmm_read(genuineGMM, 'F:/NCSISC/workspace/NCSISC/ASV/CIMFCC_GMM/gmm/genuineGMM.h5')
    result_io.gmm_read(spoofGMM, 'F:/NCSISC/workspace/NCSISC/ASV/CIMFCC_GMM/gmm/spoofGMM.h5')

    return genuineGMM, spoofGMM

if __name__ == '__main__':
    genuineGMM, spoofGMM = loadGMMs()

    print(estimate(sys.argv[1], genuineGMM, spoofGMM))