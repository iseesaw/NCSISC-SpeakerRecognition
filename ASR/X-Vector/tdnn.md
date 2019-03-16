### 模型设定: x-vector + lda + plda    
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