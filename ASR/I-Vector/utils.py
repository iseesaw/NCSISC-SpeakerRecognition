# -*- coding: utf-8 -*-
'''
数据集


数据预处理
tv_idmap.h5 训练数据(i-vector), 用于EM估计全局差异空间矩阵T(total-variablity matrix)
plda_male_idmap 训练数据(plda), 用于EM估计
enroll_idmap.h5 说话人注册数据, 训练说话人相关GMM
test_idmap.h5 测试数据(leftids, rightids)
test_ndx.h5 测试数据(modelset, segset, trialmask)
test_key.h5 测试数据(modelset, segset, tar, non)
'''

# -*- coding: utf-8 -*-
'''
GMM-UBM训练
并调参给出统计信息
'''
# 加载需要的python包
import sidekit
import os
import sys
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

def extract(file):
    '''
    '''
    with open(file) as f:
        ubmList = f.read().split('\n')

    ######### 创建FeaturesExtractor对象并提取语音集合的声学特征 ##########
    print('Initialize FeaturesExtractor')
    extractor = sidekit.FeaturesExtractor(
        audio_filename_structure='wavs_cd/test/{}.wav',
        feature_filename_structure='features_cd/test/{}.h5',
        sampling_frequency=16000,
        lower_frequency=133.3333,
        higher_frequency=6955.4976,
        filter_bank='log',
        filter_bank_size=40,
        window_size=0.025,
        shift=0.01,
        ceps_number=20,
        vad='snr',
        snr=40,
        pre_emphasis=0.97,
        save_param=['cep'], #'vad', 'energy',
        keep_all_features=False
    )

    show_list = np.asarray(ubmList)
    channel_list = np.zeros_like(show_list, dtype=int)
    
    print('Extract features and save to disk')
    extractor.save_list(
        show_list=show_list,
        channel_list=channel_list,
    )

if __name__ == '__main__':
    s = time.time()
    extract('wavs_cd/test_list.txt')
    print(time.time() - s)