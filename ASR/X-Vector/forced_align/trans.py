# -*- coding: utf-8 -*-
import os
import librosa
import textgrid
import tgt
import scipy.io.wavfile as wav
from pydub import AudioSegment
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS

num2py = {
    '0': 'ling2',
    '1': 'yi1',
    '2': 'er4',
    '3': 'san1',
    '4': 'si4',
    '5': 'wu3',
    '6': 'liu4',
    '7': 'qi1',
    '8': 'ba1',
    '9': 'jiu3',
}

py2num = {
    'ling2': 0,
    'yi1': 1,
    'er4': 2,
    'san1': 3,
    'si4': 4,
    'wu3': 5,
    'liu4': 6,
    'qi1': 7,
    'ba1': 8,
    'jiu3': 9,
}


def resample():
    for file in os.listdir('numbers/CH'):
        if '.wav' in file:
            print(file)
            file = 'numbers/CH/' + file
            y, sr = librosa.load(file, sr=22050)
            y_8k = librosa.resample(y, sr, 16000)
            librosa.output.write_wav(file, y_8k, 16000)


def read(file):
    with open(file, 'r') as f:
        line = f.readlines()[0].strip('\n')

    return line


def write(line, file):
    with open(file, 'w', newline='\n') as f:
        f.write(line + '\n')


def number2pinyin(numbers):

    return ' '.join(num2py[w] for w in numbers)


def labfileTrans():
    for file in os.listdir('numbers/CH'):
        if '.lab' in file:
            f = 'numbers/CH/' + file
            line = read(f)
            write(number2pinyin(line), f)


def use_textgrid(textgridfile):
    tg = textgrid.TextGrid.fromFile(textgridfile)
    return tg


def get_filename(file):
    idx = 0
    while os.path.exists(file.format(idx)):
        idx += 1
    return file.format(idx)


def slice_wav(audiofile, textgridfile, out_dir):
    '''获得一维数组、数组长度与读取的有关, librosa默认22050; wav默认16000'''
    #y, r = librosa.load('examples/CH/774.wav', sr=16000)
    # print(y.shape)
    #r, y = wav.read('examples/CH/774.wav')
    # print(y.shape)

    '''读取录音文件和textgrid文件, 切分音频并保存到out_dir中'''

    sound = AudioSegment.from_file(audiofile)

    tg = use_textgrid(textgridfile)
    for i, seg in enumerate(tg[0]):
        start, end, mark = seg.minTime, seg.maxTime, seg.mark
        print(mark)
        if mark != "":
            start = int(start * 1000)
            end = int(end * 1000)
            if tg[0][i + 1].mark == "":
                end = int(tg[0][i + 1].maxTime * 1000)

            audioseg = sound[start:end]

            name = get_filename("{}/{}".format(out_dir, mark) + "_{}.wav")

            audioseg.export(name, format="wav")
            print('save {}...'.format(name))

def silence_remove(file):
    fs, x = aIO.readAudioFile(file)
    segments = aS.silenceRemoval(x, fs, 0.020, 0.020, smoothWindow= 1.0, weight=0.3, plot=True)

if __name__ == '__main__':
    # resample()
    # labfileTrans()
    # # use_tgt()
    # slice_wav('numbers/CH/10061191.wav',
    #           'numbers_/10061191.TextGrid', 'numbers_')
    silence_remove('numbers/CH/10061191.wav')