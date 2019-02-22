# -*- coding: utf-8 -*-
'''
数据准备
'''
import numpy as np
import sidekit
import os
import sys
import re
import random
import pandas as pd

##### Database: ST-CMDS-20170001_1-OS  #####
dirPath = 'D:\\Project\\信息安全竞赛\\asv\\asr\\database\\ST-CMDS-20170001_1-OS\\ST-CMDS-20170001_1-OS\\'
# audioDir - Session
# 05d - Speaker ID
audioDir = "20170001P{:05d}A{:04d}"


def get_ubm_list(personN, sessionN):
    '''
    UBM模型训练的语音集合
    后续对集合内所有语音提取特征
    保存到ubm_list.txt

    :param personN, speaker id from 1 to personN
    :param sessionN, session id from 1 to N
    '''
    ubm_list = []
    for p in range(1, personN):
        for t in range(1, sessionN):
            ubm_list.append(audioDir.format(p, t))

    return np.asarray(ubm_list)


def get_enroll_list(person, sessionN):
    '''
    注册用户数据

    :param person, speaker id to enroll
    :param session, session id from 1 to N to enrolls
    '''
    enroll_list = []
    for t in range(1, 10):
        enroll_list.append(audioDir.format(52, t))
    return np.asarray(enroll_list)



def save_IdMap():
    '''
    创建IdMap对象
    attrs:
        - leftids: 语音名称
        - rightids: 说话者ID/其他ID
        - stop / start: 音频段边界

    model模型 - segment语音关联
        idmap.leftids = numpy.array(["model_1", "model_2", "model_2"])
        idmap.rightids = numpy.array(["segment_1", "segment_2", "segment_3"])
        语音的起始(全部使用则标识为None)
        idmap.start = numpy.empty((3), dtype="|O")
        idmap.stop = numpy.empty((3), dtype="|O")
        idmap.validate()
    '''
    Enroll = []

    # Create the list of models and enrollment sessions
    models = []
    segments = []
    for idx, mod in enumerate(Enroll[0]):
        models.extend([mod, mod, mod])
        segments.extend([Enroll[1][idx], Enroll[2][idx], Enroll[3][idx]])

    # Create and fill the IdMap with the enrollment definition
    enroll_idmap = sidekit.IdMap()
    enroll_idmap.leftids = np.asarray(models)
    enroll_idmap.start = np.empty(enroll_idmap.rightids.shape, '|O')
    enroll_idmap.stop = np.empty(enroll_idmap.rightids.shape, '|O')
    enroll_idmap.validate()
    enroll_idmap.write('task/trn.h5')


def save_Ndx():
    '''
    创建Ndx对象存储实验索引信息
    attrs:
        - modelset: 模型集合
        - segset: 语音集合
        - trialmask: 布尔矩阵(m, s)

    trialmask(i, j): 在模型i上评估语音j
    '''


def save_Key():
    '''
    创建Key对象存储实验信息
    attrs:
        - modelset: 模型集合
        - segset: 语音集合
        - tar: 布尔矩阵, 目标
        - non: 布尔矩阵, 非目标
    模型 i和段 j之间的测试是目标, 则tar(i, j)为真
    模型 i和段 j之间的测试是非目标的, 则non(i, j)为真

    '''

if __name__ == '__main__':
    '''
    '''
