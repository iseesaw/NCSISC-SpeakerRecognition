# -*- coding: utf-8 -*-
'''
使用pyvad库进行端点检测并进行相关截取计算
测试代码
'''
from pyvad import vad, trim
import librosa
import matplotlib.pyplot as plt
import numpy as np
import librosa.effects
from logmmse import logmmse
import scipy.io.wavfile


def load_audio():
    '''
    显示语音波形图
    :return: None
    '''
    data, fs = librosa.load('audios/zhp_1234_1.m4a')

    # time = np.linspace(0, len(data) / fs, len(data))
    # plt.plot(time, data)

    # 得到静音(很难得到没有噪声的语音)
    # data, index = librosa.effects.trim(data)
    # 降噪处理
    # data = logmmse(data, fs)
    # 端点检测
    # data = trim(data, fs, hoplength=30, vad_mode=3)
    # 向量保存
    # scipy.io.wavfile.write('audios/noise1_vad.m4a', fs, data)

    time = np.linspace(0, len(data) / fs, len(data))
    plt.plot(time, data)

    plt.show()


def do_vad():
    '''
    端点检测结果可视化
    将端点检测结果用红色边界线标识
    :return: None
    '''
    addr = 'D:\\Project\\信息安全竞赛\\asv\\asr\\references\\free-spoken-digit-dataset\\recordings\\'
    # 'audios/arctic_a0007.wav'
    data, fs = librosa.load('audios/zhp_1234_1.m4a')
    time = np.linspace(0, len(data) / fs, len(data))  # time axis

    # 端点检测
    vact = vad(data, fs, fs_vad=16000, hoplength=30, vad_mode=3)


    fig, ax1 = plt.subplots()

    # 语音波形图
    ax1.plot(time, data, color='b', label='speech waveform')
    ax1.set_xlabel("TIME [s]")

    ax2 = ax1.twinx()
    # 端点检测
    ax2.plot(time, vact, color="r", label='vad')
    plt.yticks([0, 1], ('unvoice', 'voice'))
    ax2.set_ylim([-0.01, 1.01])

    plt.legend()
    plt.show()


def do_trim():
    '''
    对语音进行端点检测并截取
    显示截取后语音波形图
    :return: None
    '''
    addr = 'D:\\Project\\信息安全竞赛\\asv\\asr\\references\\free-spoken-digit-dataset\\recordings\\'

    data, fs = librosa.load(addr + '0_jackson_0.wav')
    # vact = vad(data, fs, fs_vad=16000, hoplength=30, vad_mode=3)
    trimed = trim(data, fs, fs_vad=16000, hoplength=30, vad_mode=3)

    time = np.linspace(0, len(trimed) / fs, len(trimed))  # time axis
    fig, ax1 = plt.subplots()

    ax1.plot(time, trimed, color='b', label='speech waveform')
    ax1.set_xlabel("TIME [s]")

    plt.show()


if __name__ == '__main__':
    # do_vad()
    load_audio()
