import os
import sys
from config import *


def generate(username):
    loginpath = 'userdata/{}/login'.format(username)
    scorepath = 'userdata/{}/score'.format(username)
    attackpath = 'userdata/{}/attack'.format(username)
    if not os.path.exists(loginpath):
        os.mkdir(loginpath)
    if not os.path.exists(scorepath):
        os.mkdir(scorepath)
    if not os.path.exists(attackpath):
        os.mkdir(attackpath)

    filepath = dirpath + '/{}_login'
    f1 = open('userdata/{}/attack/utt2spk'.format(username), 'w', newline='\n')
    f2 = open('userdata/{}/attack/wav.scp'.format(username), 'w', newline='\n')
    utt2spk = '{}-{}_login {}'.format(username,
                                      username, username)
    wavscp = '{}-{}_login {}.wav'.format(
        username, username,  filepath.format(username))

    f1.write(utt2spk + '\n')
    f2.write(wavscp + '\n')

    f1.close()
    f2.close()

    with open('userdata/{}/score/trials'.format(username), 'w', newline='\n') as f:
        f.write('{} {}-{}_login target'.format(username, username, username))


def login(username):
    generate(username)

    os.system('bash login.sh {}'.format(username))

    with open('userdata/{}/score/login.scores'.format(username), 'r') as f:
        line = f.readlines()

    score = float(line[0].strip().split(' ')[2])

    if score > threshold:
        print('Yes, {:.4f}'.format(score))
    else:
        print('No, {:.4f}'.format(score))

if __name__ == '__main__':
    username = sys.argv[1]
    login(username)
