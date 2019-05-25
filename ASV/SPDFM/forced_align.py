import subprocess
import os
import sys
import settings

DICT_PATH = os.path.join(settings.ROOT_DIR_PATH, './align-conf/CH_number.txt')
MODEL_PATH = os.path.join(settings.ROOT_DIR_PATH, './align-conf/CH_number.zip')
ALIGNER_PATH = os.path.join(settings.ROOT_DIR_PATH, './montreal-forced-aligner/bin/mfa_align.exe')

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


def generateLab(wavFiledir):
    """

    :param wavFiledir: the dir contains all .wav need to generate .lab for forced align
    :return:
    """
    files = os.listdir(wavFiledir)
    for file in files:
        if not os.path.isdir(file):
            model = file.rstrip().split('_')[0]
            model = model[::-1]
            key = model[3:]
            prefix = file.rstrip().split('.')[0]
            with open(os.path.join(wavFiledir, prefix+'.lab'), 'w') as f1:
                pinyin = ''
                for idx, number in enumerate(key):
                    if idx == 0:
                        pinyin = pinyin + num2py[number]
                    else:
                        pinyin = pinyin + ' ' + num2py[number]
                f1.write(pinyin)


def align(input_dir, output_dir):
    command = ALIGNER_PATH + ' ' + input_dir + ' ' + DICT_PATH + ' ' + MODEL_PATH + ' ' + output_dir
    subprocess.call(command)

"""
    Usage: python3 forced_align.py [wavFileDir]
    assume dir like this:
    enroll
    |--15545577320 [have before execute]
    |  |--enroll1.wav [have before execute]
    |  |--enroll1.lab
    |  |--...
    |  |--...
    |--TextGrid
"""
if __name__ == '__main__':
    wavFileDir = sys.argv[1]
    generateLab(wavFileDir)
    align(wavFileDir, os.path.join(wavFileDir, '../TextGrid'))




