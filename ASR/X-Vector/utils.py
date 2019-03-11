# -*- coding: utf-8 -*-
'''
数据预处理
训练数据
ST2017 100males 100females 5segs

=====>>>>>
Input: frames + {-5, +5}
Output: #200
'''
import numpy as np
import os
import h5py

def reade_txt(file):
    with open(file, 'r') as f:
        lines = f.read().split('\n')
    return lines

def write_txt(lines, file):
    with open(file ,'w', newline='\n') as f:
        for line in lines:
            f.write(line + '\n')

def read_h5(file):
    f = h5py.File(file, 'r')
    mfcc = f['cep'][:]
    f.close()
    return mfcc

def reset():
    '''
    重组语音帧输出
    '''

def load_data():
    '''
    names.data (100m + 100f) 5segs
    ==>>
    names.h5
    ==>>
    60mfcc * Nframes
    ==>>
    X = 60mfcc * (N-10)frames
    Y = ids
    '''
    names = read('names.data')

    X, Y = [], []
    #for name in names:
