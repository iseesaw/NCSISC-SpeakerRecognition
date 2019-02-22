import os
import shutil

'''
    Process the orgin data set to the type that sidekit can use.
    all .wav files in the origin dataset to the dest dir 'TI_dataset' with 
    identification info sidekit can use. That is the list that all .wav contains
    , the enroll file includes identification info, the test file giving info about 
    each model test what data and the label file giving info about which data is target
    for the model.
'''

srcDirPath = './development_set'
destDirPath = './TI_dataset'

speakerUttDict = dict()
enrollDict = dict()
testDict = dict()

UttList = []

for dir in os.listdir(srcDirPath):
    if os.path.isdir(os.path.join(srcDirPath, dir)) and dir not in speakerUttDict.keys():
        userName = dir.split('-')[0]
        speakerUttDict[userName] = []
        enrollDict[userName] = []
        testDict[userName] = []

    wavPath = srcDirPath + '/' + dir + '/wav/'
    wavNum = len(os.listdir(wavPath))
    cnt = 0
    for f in os.listdir(wavPath):
        cnt = cnt + 1
        name, suf = os.path.splitext(f)
        speakerUttDict[userName].append(name)
        shutil.copyfile(os.path.join(wavPath, f), os.path.join(destDirPath, f))
        if cnt <= 3:
            enrollDict[userName].append(name)
        else:
            testDict[userName].append(name)
        UttList.append(name)


protocolPath = os.path.join(destDirPath, 'protocol')
if not os.path.isdir(protocolPath):
    os.makedirs(protocolPath)

f = open(os.path.join(protocolPath, 'total.txt'), 'w')
for item in UttList:
    f.write(item)
    f.write('\n')
f.close()

f = open(os.path.join(protocolPath, 'enroll.txt'), 'w')
for key in enrollDict:
    for item in enrollDict[key]:
        f.write(key + ' ' + item)
        f.write('\n')
f.close()

# append non-target trials 
tarFlag = dict()
Utts = list(testDict.keys())
for i in range(0, len(Utts)):
    tarFlag[Utts[i]] = []
    for item in testDict[Utts[i]]:
        tarFlag[Utts[i]].append('target')
    for j in range(0, len(Utts)):
        if not i == j:
            testDict[Utts[i]].append(enrollDict[Utts[j]][0])
            tarFlag[Utts[i]].append('nontarget')

f = open(os.path.join(protocolPath, 'test.txt'), 'w')
for key in testDict:
    for item in testDict[key]:
        f.write(key + ' ' + item)
        f.write('\n')
f.close()

f = open(os.path.join(protocolPath, 'label.txt'), 'w')
for key in testDict:
    for i in range(0, len(testDict[key])):
        f.write(key + ' ' + testDict[key][i] + ' ' + tarFlag[key][i])
        f.write('\n')
f.close()

