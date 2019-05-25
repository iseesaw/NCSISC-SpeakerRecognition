# -*- coding: utf-8 -*-
'''
降噪处理测试代码
'''
from logmmse import logmmse
import librosa
import scipy.io.wavfile as sio


def noise_reduct():
    '''
    降噪处理并保存
    :return: None
    '''
    data, fs = librosa.load('audios/zky_1234_0.m4a')
    out = logmmse(data, sampling_rate=fs)
    sio.write('audios/logmmse.wav', fs, out)


if __name__ == '__main__':
    noise_reduct()
