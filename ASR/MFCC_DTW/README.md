## MFCC + DTW
Ref: 基于梅尔频率倒谱系数与动态时间规整的安卓声纹解锁系统(./refs/*.pdf)

### Python库
>Details at 'ASR/文本相关的声纹识别算法.pdf'

1. ```librosa.load()``` -> ```librosa.feature.mfcc()``` -> ```mfcc.T```

2. ```dtw.dtw()``` -> ```dist```

3. ```logmmse.logmmse``` -> ```noise reduction```

4. ```pyvad.trim``` -> ```vad```

5. ```scipy.io.wavfile.write``` -> ```numpy save as wavfile``` 

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

### TODO
>Details at 'ASR/文本相关的声纹识别算法.pdf'

1. 阈值效果待验证
2. 降噪处理、端点检测效果待验证
3. 更多数据待验证