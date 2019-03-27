'''
用户注册程序
'''
import os
import sys
from config import *

def generate(username):
    filepath = dirpath+'/{}_enroll_{}'

    if not os.path.exists('userdata/' + username):
        os.mkdir('userdata/' + username)
        os.mkdir('userdata/{}/data'.format(username))

    f1 = open('userdata/{}/data/utt2spk'.format(username), 'w', newline='\n')
    f2 = open('userdata/{}/data/wav.scp'.format(username), 'w', newline='\n')
    for idx in range(3):
        idx += 1
        utt2spk = '{}-{}_enroll_{} {}'.format(username,
                                              username, idx, username)
        wavscp = '{}-{}_enroll_{} {}.wav'.format(
            username, username, idx, filepath.format(username, idx))

        f1.write(utt2spk + '\n')
        f2.write(wavscp + '\n')

    f1.close()
    f2.close()


def enroll(username):
    '''
    根据注册用户名获取注册语音
    prepare.py生成注册语音配置文件
    enroll.sh进行注册语音向量提取并保存到userdata/username
    '''
    #try:
        
    generate(username)
    os.system('bash enroll.sh {}'.format(username))
    # except:
    #     print('No')


if __name__ == '__main__':
    username = sys.argv[1]
    enroll(username)
