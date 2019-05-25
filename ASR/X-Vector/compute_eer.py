# -*- coding: utf-8 -*-
'''
读取exp/scores_enroll_test以及annotation.json
调用sklearn相关函数计算eer
'''
import json
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc


def read_txt(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.read().split('\n')
    return lines


def read_anno():
    annotation = pd.read_csv('files/annotation.csv')
    anno = {}
    for fileid, isMember in zip(annotation['FileID'], annotation['IsMember']):
        anno[fileid] = isMember
    return anno


def get_y_true():
    '''one model'''
    submit = pd.read_csv('output/submit.csv')
    dic = read_anno()

    y, y_pred = [], []
    for file, ism in zip(submit['FileId'], submit['IsMember']):
        y_pred.append(ism)
        y.append(1 if dic[file] == 'Y' else 0)

    return y, y_pred


def compute():
    y, y_pred = get_y_true()

    fpr, tpr, threshold = roc_curve(y, y_pred, pos_label=1)
    fnr = 1 - tpr
    eer_threshold = threshold[np.nanargmin(np.absolute((fnr - fpr)))]

    eer = fpr[np.nanargmin(np.absolute((fnr - fpr)))]

    info = 'eer_threshold = {:.2f}\neer={:.2f}%'.format(
        eer_threshold, eer * 100)
    
    print(info)

    num = 0
    for r, s in zip(y, y_pred):
        if r and s > eer_threshold:
            num += 1
        if not r and s < eer_threshold:
            num += 1
    print(num / len(y))

if __name__ == '__main__':
    compute()
