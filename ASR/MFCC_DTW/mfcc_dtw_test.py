# -*- coding: utf-8 -*-
'''
特征提取
MFCC
DTW计算
测试代码
'''
import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
import numpy as np
from pyvad import trim
from logmmse import logmmse
import python_speech_features

def audio2mfcc(audiofile):
    '''
    从.wav语音文件中提取特征
    MFCC
    :return: mfcc
    '''
    y, sr = librosa.load(audiofile, sr=None)

    # 降噪处理
    #y = logmmse(y, sr)
    # 端点检测
    #y = trim(y, sr, hoplength=30, vad_mode=3)
    mfccs = python_speech_features.mfcc(y, sr, nfft=1536)

    #mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=32)
    # delta = librosa.feature.delta(mfccs)

    return mfccs  # , delta


def show_mfcc():
    '''
    显示MFCC能量图
    '''
    audio1 = 'audios/1234.m4a'
    # audio2 = 'audios/1234(1).m4a'
    mfcc1 = audio2mfcc(audio1)
    # mfcc2 = audio2mfcc(audio2)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc1, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()


def comp_dtw(p1=None, p2=None, d=None, i=None):
    '''
    Input: 两段语音的MFCC特征向量
    Output: 两个MFCC特征向量的DTW距离
    '''
    addr = 'D:\\Project\\信息安全竞赛\\asv\\asr\\references\\free-spoken-digit-dataset\\recordings\\'
    # jackson, nicolas, theo, yweweler
    # audio1 = addr + '{}_{}_{}.wav'.format(d, p1, i)
    # audio2 = addr + '{}_{}_{}.wav'.format(d, p2, i + 1)

    audio1 = 'audios/zky_1234_0.m4a'
    audio2 = 'audios/zky_1234_3.m4a'

    mfcc1 = audio2mfcc(audio1)
    mfcc2 = audio2mfcc(audio2)

    x, y = mfcc1, mfcc2
    print(x.shape, y.shape)
    lam = lambda x, y: np.linalg.norm(x - y, ord=2)
    dist, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=lam)

    print(dist)
    # print(cost_matrix)
    # print(acc_cost_matrix)
    # print(mfcc1.shape, len(path[0]))
    # print(mfcc2.shape, len(path[1]))
    # print(path[0])
    # print(path[1])
    # plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    # plt.plot(path[0], path[1], 'w')
    # plt.show()
    #
    # return dist


def comp_threshold():
    '''
    4个人、10个数字、重复50遍
    相同人、不同人计算阈值

    threshold 50
    accuN 1889
    totalN 2000
    accu 0.9445
    :return:
    '''
    persons = ['jackson', 'nicolas', 'theo', 'yweweler']
    accu = [0, 0, 0]
    total = [0, 0, 0]
    for p1 in range(4):
        for p2 in range(4):
            if p2 >= p1:
                for d in range(10):
                    for i in range(20):
                        dist = comp_dtw(persons[p1], persons[p2], d, i)
                        if p1 == p2:
                            total[0] += 1
                            if dist < 50:
                                accu[0] += 1

                        if p1 != p2:
                            total[1] += 1
                            if dist > 50:
                                accu[1] += 1
                        print('Ok!' if dist < 50 else 'Bad!', persons[p1], i, persons[p2], i + 1, d, dist)

    accu[2] = accu[0] + accu[1]
    total[2] = total[0] + total[1]
    print('同一人正确率', accu[0] / total[0])
    print('不同人正确率', accu[1] / total[1])
    print('正确率', accu[2] / total[2])
    '''
    同一人正确率 0.9275
    不同人正确率 0.9558
    正确率 0.9445
    '''


if __name__ == '__main__':
    # comp_threshold()
    comp_dtw()
