# -*- coding: utf-8 -*-
'''
将语音文件按照enroll和test分别拆分为data/enroll data/test
根据annotation文件生成trials文件(speaker/ uttr/ target or nontarget)异或随机生成target以获得最后打分

'''
import os
import shutil
import json
import numpy as np
import random
from xvector2cosin_score import *


def move_enroll_test(files, dest):
    # 将语音文件分别移到data下的train和test文件夹中
    for file in files:
        shutil.copyfile('wav/{}.wav'.format(file),
                        'futurelab/{}/{}.wav'.format(dest, file))


def enroll_test(groupid):
    '''
    生成enroll.txt 和test.txt(wav speakerid)文件
    用于使用bash enroll.sh提取xvector
    '''
    group = 'group{}'.format(groupid)

    annotation = load_json('files/annotation.json')

    enroll = load_json('files/enroll.json')
    enroll_files = []
    for key in enroll[group].keys():
        for file in enroll[group][key]['FileID']:
            line = './futurelab/enroll/{}.wav {}'.format(file, key)
            enroll_files.append(line)
    write_txt(enroll_files, 'files/enroll.txt')

    test = load_json('files/test.json')
    test_files = []
    for key in test[group].keys():
        speaker = annotation[group][key]['SpeakerID']
        line = './futurelab/test/{}.wav {}'.format(key, speaker)
        test_files.append(line)

    write_txt(test_files, 'files/test.txt')


def trials(groupid):
    '''
    生成trialds文件(speakerid uttrid)
    用于plda计算分数
    '''
    group = 'group{}'.format(groupid)

    enroll = load_json('files/enroll.json')
    test = load_json('files/test.json')
    annotation = load_json('files/annotation.json')

    lines = []
    for enrollKey in enroll[group].keys():
        for testKey in test[group].keys():
            testId = annotation[group][testKey]['SpeakerID'] 
            if testId == enrollKey:
                target = 'target'
            else:
                target = 'nontarget'
            line = '{} {}-{} {}'.format(enrollKey, testId,testKey, target)
            lines.append(line)

    write_txt(lines, 'files/trials')

def analysis_score_file():
    '''
    读取plda生成的score文件(speakerid uttrspeakerid-uttrfileid score)
    解析为json对象
    {
        group:{
            uttr:{
                speakid: score,
                ...
            }
        }
    }
    '''
    lines = read_txt('exp/scores_enroll_test')
    scores = {}
    for line in lines:
        items = line.split(' ')
        params = items[1].split('-')
        if params[1] not in scores:
            scores[params[1]] = {}
        scores[params[1]][items[0]] = float(items[2])
    dump_json(scores, 'exp/scores.json')

def score(groupid, threshold=0):
    '''
    传入测试组序号
    读取annotation获得测试组所有uttrfileid
    读取allscores, 获取uttrfileid的得分
    '''
    group = 'group{}'.format(groupid)


    annota_dic = load_json(dirpath + 'annotation.json')
    test_dic = load_json(dirpath + 'test.json')
    allscores = load_json('exp/scores.json')


    sps, imss, segs, scos = [], [], [], []
    s = 0
    for seg in test_dic[group].keys():
        speaker = annota_dic[group][seg]['SpeakerID']
        ism = annota_dic[group][seg]['isMember']
        sco = max(list(allscores[seg].values()))

        sps.append(speaker)
        imss.append(ism)
        segs.append(seg)
        scos.append(sco)
        if sco > threshold and ism == 'Y':
            s += 1
        if sco < threshold and ism == 'N':
            s += 1
    print('{:.1f}'.format(threshold), s / len(sps))


if __name__ == '__main__':
    #analysis_score_file()
    for i in range(6):
        #enroll_test(i)
        #trials(i)

        print('============== {} ================'.format(i))
        for j in range(0, 30, 2):
            score(i, j)