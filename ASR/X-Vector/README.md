### 挑战杯-跨设备说话人识别

模型设定: x-vector + lda + plda    
audio -> MFCC/Fbank -> context frames -> TDNN -> softmax -> output (train)    
                                            -> hidden layer output (x-vector)   
                                            -> LDA -> PLDA -> output    

### x-vector
可以先从d-vector入手

#### 数据预处理

#### 模型结构
<img src="https://img-blog.csdnimg.cn/201811071035470.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODg1ODg2MA==,size_16,color_FFFFFF,t_70">  

搭建模型过程：  
- Input: filterbank(24,) + context{-2, +2}, 120x512  
- Layer2: TDNN, 1536x512  
- Layer3: TDNN, 1536x512  
- Layer4: Dense, 512x512  
- Layer5: Dense, 512x1500  
- Layer6: Stats Pooling, 1500Tx512  
- Layer7: Dense, 3000x512 ==>>> x-vector ==>>> LDA(512x150) ==>>> PLDA  
- Layer8: Dense, 512x512  
- Layer9: softmax, 512xN  

>处理细节  
> 
> - 多个相邻帧作为输入, 每个输入产生一个x-vector, 然后可以求平均值或求和获得语音的x-vector  [Ref](https://github.com/mravanelli/SincNet/issues/10)
> - ...
>   
>More: VAD、噪声增强、去除过短utt、去除utt少的speaker

Ref  
(Already Reading)   
1. [DEEP NEURAL NETWORKS FOR SMALL FOOTPRINT TEXT-DEPENDENT SPEAKER VERIFICATION](http://www.mirlab.org/conference_papers/International_Conference/ICASSP%202014/papers/p4080-variani.pdf)  
d-vector生成细节, 包括输入设置、神经网络参数etc.

(Need to read)  
1. [X-VECTORS: ROBUST DNN EMBEDDINGS FOR SPEAKER RECOGNITION](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf)  
2. [End-to-End Text-Dependent Speaker Verification](http://cn.arxiv.org/pdf/1509.08062)

#### 代码实现
已实现[Demo](x_vector.py)(待处理数据测试)  

- Next
    + 数据处理、训练模型
    + TDNN可用性测试
    + stats pooling问题
    + predict部分代码

#### Ref：使用Kaldi模型
1. 准备语料训练集以及测试集，可以是不同语言越多越好
2. 使用mfcc提取特征，尝试过替换Mel-filter bank特征效果并不好，主要也没有调节各种参数
4. 利用回响和三种噪音增强了训练数据，测试了增强于非增强的效果还是非常明显
5. 这部分对增强的数据进行了随机筛选于原始数据相同数量级的数据提取特征并于原始数据结合
6. 做了归一化移除了静音帧
7. 这里移除了小于min_len时长的语音段，也舍弃了小于min_num_utts段数音频的说话人信息
8. 生成egs并训练xvector网络
9. 利用embedding层提取xvector特征
10. lda降维然后再用plda打分
11. 计算eer  
[sre16/v2](https://github.com/kaldi-asr/kaldi/tree/master/egs/sre16/v2)  
[voxceleb/v2](https://github.com/kaldi-asr/kaldi/tree/master/egs/voxceleb/v2)									

