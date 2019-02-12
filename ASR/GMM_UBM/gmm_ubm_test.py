# -*- coding: utf-8 -*-
'''
speaker_recognition
Extracing MFCC from audio: extract_mfcc_coefficients
    mfcc + delta mfcc
Creating Universal Background Model: speaker_recognition
MAP adaptation: speaker_recognition
Testing the map adapted model: testing_model

'''
import librosa
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import cdist
import pyvad
from sklearn import preprocessing
from sklearn.cluster import SpectralClustering

def extract_features():
    '''
    特征提取
    MFCC + delta MFCC
    '''
    y, sr = librosa.load('')

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    stacked = np.vstack((mfcc, mfcc_delta, mfcc_delta2))

    return stacked.T


def map_adaptation(gmm, data):
    '''
    MAP(最大后验)更新
    '''
    N = data.shape[0]
    D = data.shape[1]
    K = gmm.n_components

    mu_new = np.zeros((K, D))
    n_k = np.zeros((K, 1))

    # GMM模型参数
    # 均值mu、方差cov、每个样本属于各个高斯分布的概率pi
    mu_k = gmm.means_
    cov_k = gmm.covariances_
    pi_k = gmm.weights_

    likelihood_threshold = 1e-20
    max_iterations = 300
    relevance_factor = 16
    old_likelihood = gmm.score(data)
    new_likelihood = 0
    iterations = 0
    while (abs(old_likelihood - new_likelihood) > likelihood_threshold and iterations < max_iterations):
        iterations += 1
        old_likelihood = new_likelihood
        z_n_k = gmm.predict_proba(data)
        n_k = np.sum(z_n_k, axis=0)

        for i in range(K):
            temp = np.zeros((1, D))
            for n in range(N):
                temp += z_n_k[n][i] * data[n, :]
            mu_new[i] = (1 / n_k[i]) * temp

        adaptation_coefficient = n_k / (n_k + relevance_factor)
        for k in range(K):
            mu_k[k] = (adaptation_coefficient[k] * mu_new[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])
        gmm.means_ = mu_k

        log_likelihood = gmm.score(data)
        new_likelihood = log_likelihood
        print(log_likelihood)
    return gmm


def main():
    # 参数设置
    SR = 8000  # sample rate
    N_MFCC = 13
    N_FFT = 0.032
    HOP_LENGTH = 0.010

    N_COMPONENTS = 16  # number of gaussians
    COVARINACE_TYPE = 'full'

    y = []
    LOAD_SIGNAL = False
    if LOAD_SIGNAL:
        y, sr = librosa.load('')
        pre_emphasis = 0.97
        y = np.append(y[0], y[1:] - pre_emphasis * y[:-1])

    ubm_features = extract_features()
    ubm_features = preprocessing.scale(ubm_features)

    ubm = GaussianMixture(n_components=N_COMPONENTS, covariance_type=COVARINACE_TYPE)
    ubm.fit(ubm_features)

    print(ubm.score(ubm_features))

    SV = []

    for i in range(101):
        f_ = extract_features()
        f_ = preprocessing.scale(f_)
        gmm = map_adaptation(gmm, f_, )

        sv = gmm.means_.flatten()
        sv = preprocessing.scale(sv)
        SV.append(sv)

    SV = np.array(SV)
    print(SV.shape)

    N_ClUSTERS = 2

    sc = SpectralClustering(n_clusters=N_ClUSTERS, affinity='cosine')
    labels = sc.fit_predict(SV)