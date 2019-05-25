'''
读取exp/enroll_test_score文件, 解析得到每个fileid的得分并判断
'''
import os
import sys
import numpy as np


def analysis(scorespath, outputdir):
    with open(scorespath, 'r') as f:
        lines = f.readlines()

    score_dic = {}
    for line in lines:
        params = line.split(' ')
        if len(params) > 2:
            file = params[1].split('-')[1]
            if file not in score_dic:
                score_dic[file] = []
            score_dic[file].append(float(params[2]))

    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    with open(outputdir + '/submit.csv', 'w', newline='\n', encoding='utf-8') as f:
        f.write('FileId,IsMember\n')
        for key in score_dic.keys():
            score = np.max(np.array(score_dic[key]))
            f.write('{},{}\n'.format(key, score))

if __name__ == '__main__':
    scorespath = sys.argv[1]
    outputdir = sys.argv[2]
    analysis(scorespath, outputdir)
