## MFCC + DTW
### Python库
1. ```librosa.load()``` -> ```librosa.feature.mfcc()``` -> ```mfcc.T```

2. ```dtw.dtw()``` -> ```dist```

### 语音数据集
>Req: 文本相关、短语(数字串)  

1. *#English 类别：commands, names, numbers； 不同人语音不重复*  
>local: .\asv\asr\references\word-recogniton  

2. *#English 4个人, 0-9, 每个数字重复50遍*  
>local: .\asv\asr\references\free-spoken-digit-dataset\recordings  
>threshold = 50, accuN = 1889, totalN = 2000, accu = 0.9445

3. *#English 15个人, 0-9, 每个数字重复3遍*  
>loacal: .\asv\asr\references\AudioDigitRecognition\TRAIN  

4. *n个人, m段数字串(四字短语、诗、英语), 重复l遍*  
>不同人对同一内容重复多遍, 计算声纹识别dtw阈值(目前单个数字阈值: 50)  
>Win10自带录音机、安静环境下使用普通话, 1234、123456、1245678各录音3遍
>命名: 姓名_数字串_遍数.wav

| person1 | person2 | dist | dist(vad) |
| --- | --- | --- | --- |
| zky_1234_0.m4a | zky_1234_1.m4a | 46 | 57 |
| zky_1234_0.m4a | zky_1234_2.m4a | 49 | 63 |
| zky_1234_0.m4a | zky_1234_3.m4a | 77 | 69 |
| zky_1234_1.m4a | zky_1234_2.m4a | 38 | 40 |
| zky_1234_1.m4a | zky_1234_3.m4a | 62 | 59 |
| zky_1234_2.m4a | zky_1234_3.m4a | 50 | 46 |
| zhp_1234_0.m4a | zhp_1234_1.m4a | 26 | 21 |
| same | <50 | 5/7 | 3/7 |
| same(ex 0) | <50 | 3/4 | 3/4 |
| zky_1234_0.m4a | zhp_1234_0.m4a | 40 | 63 |
| zky_1234_0.m4a | zhp_1234_1.m4a | 44 | 55 |
| zky_1234_1.m4a | zhp_1234_0.m4a | 46 | 49 |
| zky_1234_1.m4a | zhp_1234_1.m4a | 49 | 50 |
| zky_1234_2.m4a | zhp_1234_0.m4a | 49 | 57 |
| zky_1234_2.m4a | zhp_1234_1.m4a | 56 | 60 |
| zky_1234_3.m4a | zhp_1234_0.m4a | 76 | 71 |
| zky_1234_3.m4a | zhp_1234_1.m4a | 78 | 73 |
| diff | >50 | 3/8 | 7/8 |
| total | - | 8/15 | 10/15 |
| diff(ex 0) | >50 | 3/6 | 5/6 |
| total(ex 0) | - | 6/10 | 8/10 |