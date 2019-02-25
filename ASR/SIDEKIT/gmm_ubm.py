# -*- coding: utf-8 -*-
'''
GMM-UBM
'''
# 加载需要的python包
import sidekit
import os
import sys
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np

# 设置宏常量参数
distribNb = 512
# 多线程个数
nbThread = max(multiprocessing.cpu_count() - 1, 1)

##### Database: ST-CMDS-20170001_1-OS  #####
dirPath = 'D:\\Project\\信息安全竞赛\\asv\\asr\\database\\ST-CMDS-20170001_1-OS\\ST-CMDS-20170001_1-OS\\'
audioDir = "20170001P{:05d}A{:04d}"


#############################################

def extract_feature():
    '''
    FeatureExtractor
    :return:
    '''


def train_ubm():
    '''
    '''
    print('Load task definition')
    enroll_idmap = sidekit.IdMap('task/trn.h5')
    test_ndx = sidekit.Ndx('task/ndx.h5')
    #key = sidekit.Key('task/key.h5')

    with open('task/ubm_list.txt') as inpuFile:
        ubmList = inpuFile.read().split('\n')

    ########## 创建FeaturesExtractor对象并提取语音集合的声学特征 ##########
    # print('Initialize FeaturesExtractor')
    # extractor = sidekit.FeaturesExtractor(
    #     audio_filename_structure=dirPath + '{}.wav',
    #     feature_filename_structure='features/{}.h5',
    #     sampling_frequency=16000,
    #     lower_frequency=133.3333,
    #     higher_frequency=6955.4976,
    #     filter_bank='log',
    #     filter_bank_size=40,
    #     window_size=0.025,
    #     shift=0.01,
    #     ceps_number=19,
    #     vad='snr',
    #     snr=40,
    #     pre_emphasis=0.97,
    #     save_param=['vad', 'energy', 'cep'],
    #     keep_all_features=False
    # )
    #
    # # Get the complete list of features to extract
    # # show_list = np.unique(np.hstack([ubmList, enroll_idmap.rightids, np.unique(test_ndx.segset)]))
    # show_list = get_ubm_list()
    # channel_list = np.zeros_like(show_list, dtype=int)
    #
    # print('Extract features and save to disk')
    # extractor.save_list(
    #     show_list=show_list,
    #     channel_list=channel_list,
    #     # num_thread=nbThread
    # )

    ########## 创建FeaturesServer并读取特征 ##########
    features_server = sidekit.FeaturesServer(
        features_extractor=None,
        feature_filename_structure='features/{}.h5',
        sources=None,
        dataset_list=['energy', 'cep', 'vad'],
        mask=None,
        feat_norm='cmvn',
        global_cmvn=None,
        dct_pca=False,
        dct_pca_config=None,
        sdc=False,
        sdc_config=None,
        delta=True,
        double_delta=True,
        delta_filter=None,
        context=None,
        traps_dct_nb=None,
        rasta=True,
        keep_all_features=False
    )

    ########## 训练UBM模型并保存 ##########
    # print('Train the UBM by EM')
    ubm = sidekit.Mixture()
    # llk = ubm.EM_split(
    #     features_server,
    #     ubmList,
    #     distribNb,
    #     # num_thread=nbThread,
    #     save_partial=False
    # )
    # ubm.write('data/ubm.h5')

    ubm.read('data/ubm.h5')

    ########## 注册用户更新UBM模型 ##########

    print('Compute the sufficient statistics')
    # 创建StatServer并在注册数据上进行统计
    enroll_stat = sidekit.StatServer(
        enroll_idmap,
        distrib_nb=distribNb,
        feature_size=60
    )
    # 计算保存在stat0 stat1
    enroll_stat.accumulate_stat(
        ubm=ubm,
        features_server=features_server,
        seg_indices=range(enroll_stat.segset.shape[0]),
        num_thread=nbThread
    )
    enroll_stat.write('data/stat_enroll.h5')

    print('MAP adaptation of the speaker models')
    # 训练GMM super-vector
    regulation_factor = 3  # MAP regulation factor
    enroll_sv = enroll_stat.adapt_mean_map_multisession(ubm, regulation_factor)
    enroll_sv.write('data/sv_enroll.h5')

    print('Compute trial scores')
    # 返回Score对象
    scores_gmm_ubm = sidekit.gmm_scoring(
        ubm,
        enroll_sv,
        test_ndx,
        features_server,
        num_thread=nbThread
    )
    scores_gmm_ubm.write('data/scores_gmm_ubm.h5')


if __name__ == '__main__':
    train_ubm()
