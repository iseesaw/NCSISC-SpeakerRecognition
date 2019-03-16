# -*- coding: utf-8 -*-
'''
为使用sidekit的plda作为后端进行相关文件准备

读取数据x-vector生成IdMap、StatServer格式h5文件
IdMap -->> StatServer
plda_xv.h5  <<-- plda_speakers.txt
enroll_xv.h5 <<-- enroll.json groupX models uttrs
test_xv.h5 <<-- test.json
test_ndx.h5 <<-- groupX moles uttrs
'''
import sidekit
from xvector2cosin_score import *


def save_statserver(modelset, segset, stat1, file):
    stat_server = sidekit.StatServer()
    print('writing {} models and {} segments to {}'.format(len(modelset), len(segset), file))
    stat_server.modelset = np.asarray(modelset)
    stat_server.segset = np.asarray(segset)
    stat_server.stat0 = np.ones((len(segset), 1))
    stat_server.stat1 = stat1
    stat_server.start = np.ones((len(segset)))*(-1)
    stat_server.stop = np.ones((len(segset)))*(-1)
    stat_server.validate()
    stat_server.write(file)


def save_Ndx(models, segments, file):
    Nmodels, Nsegments = len(models), len(segments)
    print('writing {} models and {} segments {}'.format(Nmodels, Nsegments, file))
    test_ndx = sidekit.Ndx()
    test_ndx.modelset = np.asarray(models)
    test_ndx.segset = np.asarray(segments)
    test_ndx.trialmask = np.ones((Nmodels, Nsegments), dtype='bool')
    test_ndx.write(file)


def create_statserver(groupid):
    group = 'group{}'.format(groupid)

    # 获得所有语音的x-vector
    uttrs = read('c_xvector.txt')

    # enroll_xv
    print('create enroll_xv')
    enroll_dic = load_json(dirpath + 'enroll.json')
    models, segsets, stat1 = [], [], []
    for key in enroll_dic[group].keys():
        for file in enroll_dic[group][key]['FileID']:
            vector = uttrs[file]['vector']
            models.append(key)
            segsets.append(file)
            stat1.append(vector)
    save_statserver(models, segsets, np.asarray(stat1), 'plda/data/{}_enroll_xv.h5'.format(group))

    # test_xv
    print('create test_xv')
    test_dic = load_json(dirpath + 'test.json')
    models1, segsets1, stat11 = [], [], []
    for key in test_dic[group].keys():
        vector = uttrs[key]['vector']
        models1.append('who')
        segsets1.append(key)
        stat11.append(vector)
    save_statserver(models1, segsets1, np.asarray(stat11), 'plda/data/{}_test_xv.h5'.format(group))

    save_Ndx(np.unique(np.asarray(models)), segsets1, 'plda/data/{}_test_ndx.h5'.format(group))

    if not groupid:
        uttrs = read('plda_xvector.txt')
        models, segsets, stats1 = [], [], []
        for key in uttrs.keys():
            models.append(uttrs[key]['speaker'])
            segsets.append(key)
            stats1.append(uttrs[key]['vector'])
        save_statserver(models, segsets, np.asarray(stats1), 'plda/data/plda_xv.h5')


if __name__=='__main__':
    for i in range(6):
        create_statserver(i)