# -*- coding: utf-8 -*-
'''
声纹识别正式版代码
MFCC(梅尔频率倒谱系数) + DTW(动态时间规整)
+ 降噪处理、端点检测
'''
import librosa
from dtw import dtw
import numpy as np
import scipy.io.wavfile
from logmmse import logmmse
from pyvad import trim


def audio2mfcc(addr):
    '''
    语音保存地址
    :return: mfcc特征
    '''
    y, sr = librosa.load(addr, sr=None)

    # 降噪
    # y = logmmse(y, sr)
    # 端点检测
    # y = trim(y, sr, hoplength=30, vad_mode=3)
    # numpy保存为wavfile
    # scipy.io.wavfile.write('audios/noise1_vad.m4a', sr, y)

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=30)
    return mfccs


def mfcc2dtw(mfcc1, mfcc2):
    '''
    :param mfcc1, mfcc2 注册语音mfcc和登陆语音mfcc
    :return: dist mfcc1和mfcc2的dtw距离
    '''
    x, y = mfcc1.T, mfcc2.T

    lam = lambda x, y: np.linalg.norm(x - y, ord=2)
    dist, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=lam)
    return dist


def main():
    '''
    读取语音: 语音库注册语音、登陆语音
    计算语音MFCC特征向量
    对MFCC特征向量进行DTW计算得出距离
    根据阈值判断是否属于一个人
    :return: True if logining name and audio is consistent, otherwise False
    '''
    name = 'zky'
    s_addr = 'audios/{}_1234_0.m4a'.format(name)
    s_mfcc = audio2mfcc(s_addr)

    login_addr = 'audios/{}_1234_1.m4a'.format('zhp')
    l_mfcc = audio2mfcc(login_addr)

    dist = mfcc2dtw(s_mfcc, l_mfcc)

    return True if dist < 50 else False, dist


if __name__ == '__main__':
    result, dist = main()
    print(result, dist)
