# -*- coding: utf-8 -*-
'''
根据enroll.csv和test.csv生成trials文件
根据传入testdir生成enroll.txt和attack.txt文件
'''
import sys
import json
import numpy as np
import pandas as pd
import random


def write_txt(lines, filename):
    with open('files/{}'.format(filename), 'w', newline='\n') as f:
        for line in lines:
            f.write(line + "\n")


def read_csv(testdir):
    enrollment = pd.read_csv('files/enrollment.csv')
    enroll_dic = {}
    enroll_lines = []
    for groupid, speakerid, fileid in zip(
            enrollment['GroupID'],
            enrollment['SpeakerID'],
            enrollment['FileID']):
        group = 'group{}'.format(groupid)
        if group not in enroll_dic:
            enroll_dic[group] = {}
        if speakerid not in enroll_dic[group]:
            enroll_dic[group][speakerid] = []
        enroll_dic[group][speakerid].append(fileid)

        enroll_lines.append('{}.wav {}'.format(testdir + '/' + fileid, speakerid))

    write_txt(enroll_lines, 'enroll.txt')

    test = pd.read_csv('files/test.csv')
    test_dic = {}
    test_lines = []
    for groupid, fileid in zip(test['GroupID'], test['FileID']):
        group = 'group{}'.format(groupid)
        if group not in test_dic:
            test_dic[group] = []
        test_dic[group].append(fileid)

        test_lines.append('{}.wav {}'.format(testdir + "/" + fileid, group))

    write_txt(test_lines, 'attack.txt')

    construct_trials(enroll_dic, test_dic)


def construct_trials(enroll_dic, test_dic):
    # model fileid target_or_not
    lines = []
    for group in test_dic.keys():
        for test_fileid in test_dic[group]:
            for speakerid in enroll_dic[group].keys():
                target = 'target' if random.random() > 0.5 else 'nontarget'
                lines.append('{} {}-{} {}'.format(speakerid, group,test_fileid, target))

    write_txt(lines, 'trials')

if __name__ == '__main__':
    testdir = sys.argv[1]
    print('python prepare.py {}.'.format(testdir))
    read_csv(testdir)
    print('Successfully prepare files.')
