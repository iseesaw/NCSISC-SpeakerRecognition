### DNN-HMM
- 步骤:
    + 帧长切分, 提取特征(MFCC)
    + GMM-HMM进行alignment对齐; 对每一帧进行聚类(音素总数), 获得每帧属于各个音素的概率; HMM进行解码搜索, 获得每一帧最优音素表示序列
    + DNN-HMM; 每一帧(多帧)作为DNN输入, GMM似然值(音素标签)作为输出; 训练DNN参数, ...
- 注: 关于GMM-HMM中的HMM  
![](https://pic4.zhimg.com/80/v2-d4077c2dbd9899d8896751a28490c9c7_hd.jpg)
    + 观察状态序列: 语音中的每一帧; 词性标注中的词串
    + 隐藏状态序列: 语音每一帧对应的音素; 词性标注中每个词对应的词性标签
    + 状态转移矩阵: 语音中音素之间的转移概率(*数据集计算*, GMM-HMM计算？？); 词性标注中词性之间的转移概率  
![](http://djt.qq.com/upload/public/common/2013/08/images/05170718962.jpg)
    + 发射概率矩阵: 语音中各个音素发射为每一帧的概率(*GMM似然值*, GMM-HMM获得概率输入DNN进行反向传播); 词性标注中每个词性发射为每个词的概率   
[Ref paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/dbn4lvcsr-transaslp.pdf)
    + HMM学习问题  
    给定 $\lambda = (\pi, A, B)$  
    $O_t$： 帧  
    $S_i$： 音素(隐藏状态), 隐藏状态序列待求      
    $a_{ij}$： 音素$i,j$之间的转移概率  
    $b_{i}(O_t)$： 音素$i$发射为$O_t$帧的概率  
    Baum-Welch算法(EM)计算$A, B$  
    (训练集上给定音素序列, 可以使用Viterbi算法计算, 进行forced alignment, 然后可以使用EM重复训练)

    + EM算法求解HMM  
![](https://img-blog.csdn.net/20140530200730218?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWJjamVubmlmZXI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- force alignment
给定音素序列(phoneme), 根据每一帧的GMM似然值, 

GMM-HMM -> DNN-HMM -> DNN-HMM迭代进行强制对齐. 

- embeded training
除了将词拆分为音素训练(embeded training), 也可以直接使用整个词(Whole word)进行训练  
![](http://vsooda.github.io/assets/hmmtts/isolate_embed_training.png)

