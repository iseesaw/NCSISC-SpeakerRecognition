# -*- coding: utf-8 -*-
# 生成utt2spk和wav.scp文件
# utt2spk
#   speakerid-uttid speakerid
# wav.scp
#   uttid path
# command: 
import os
import sys

if (len(sys.argv)-1) != 2:
    print("Usage: $0 <speakers.txt> <output-dir>")
    exit(1)

file = sys.argv[1]
out_dir = sys.argv[2]

utt2spk_path = out_dir + '/utt2spk'
wavscp_path = out_dir + '/wav.scp'

if (os.system("mkdir -p %s" %(out_dir)) != 0):
    print ("Error making directory %s" %(out_dir))

with open(file, 'r') as f:
    lines = f.read().split('\n')
output1 = open(utt2spk_path, 'w')
output2 = open(wavscp_path, 'w')

for line in lines:
    if len(line) < 1:
        continue
    items = line.split(' ')
    uttid = items[0].split('/')[-1].split('.')[0]
    speakid = items[1]
    utt2spk_tmp = '{}-{} {}'.format(speakid, uttid, speakid)
    # speakerid uttid uttpath
    # or uttid uttpath
    wavscp_tmp = '{}-{} {}'.format(speakid, uttid, items[0])
    output1.write(utt2spk_tmp + '\n')
    output2.write(wavscp_tmp + '\n')

output1.close()
output2.close()