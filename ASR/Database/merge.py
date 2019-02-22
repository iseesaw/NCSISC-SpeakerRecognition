from scipy.io.wavfile import read, write
import librosa
import numpy as np
from pyvad import vad, trim


def concencate(string='0123456', person='jackson', times=5):
    '''
    连接同一个人的6个数字
    '''
    #data, fs = librosa.load('audios/zky_1234_0.m4a')
    #sio.write('audios/logmmse.wav', fs, out)
    #
    path = 'D:\\Project\\信息安全竞赛\\asv\\asr\\database\\free-spoken-digit-dataset\\recordings\\{digit}_{name}_{time}.wav'

    for i in range(times):
        records = None
        flag = True
        for s in string:
            record, fs = librosa.load(path.format(digit=s, name=person, time=i))
            if flag:
                records = record
                flag = False
            else:
                records = np.concatenate((records, record), axis=0)
        dest = 'merge/{string}_{name}_{time}.wav'
        write(dest.format(string=string, name=person, time=i), fs, records)

if __name__ == '__main__':
    persons = ['jackson', 'nicolas', 'theo', 'yweweler']
    for person in persons:
        concencate(person=person)