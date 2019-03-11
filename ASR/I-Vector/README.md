### gmm-ubm i-vector plda

- i-vector.py 代码实现
- i-vector.md 相关原理
- task 
    + tv_idmap.h5 训练数据(i-vector), 用于EM估计全局差异空间矩阵T(total-variablity matrix)
    + plda_male_idmap 训练数据(plda), 用于EM估计
    + enroll_idmap.h5 说话人注册数据, 训练说话人相关GMM
    + test_idmap.h5 测试数据(leftids, rightids)
    + test_ndx.h5 测试数据(modelset, segset, trialmask)
    + test_key.h5 测试数据(modelset, segset, tar, non)
- data 
    + ubm.h5 背景数据模型
    + enroll_stat.h5 说话人注册信息
    + test_stat.h5 说话人测试信息
    + back_stat.h5 plda方程训练数据信息
    + tv_info.h5 i-vector方程数据
    + enroll_iv.h5 注册语音i-vector
    + test_iv.h5 测试语音i-vector
    + plda_iv.h5 plda方程训练i-vector
    + plda_model.h5 plda方程数据

#### 模型原理
[i-vector.md](i-vector.md)

#### 代码实现
1. 训练背景数据模型UBM(训练库)
2. 用户注册, 获得用户相关GMM
3. 训练i-vector方程(训练库)
4. 获得用户注册、登录i-vector、以及训练库语音i-vector
5. 训练plda方程(用户、训练库语音i-vector)
6. 用户测试打分

#### 测试数据
跨设备(信道差异), 使用AIshell1(高保真麦克风) + ST2007(Android或ios)  

<table>
    <tr>
        <td>dataset</td>
        <td >aishell 1 & ST2017</td>
    </tr>
    <tr>
        <td>gender</td>
        <td>120 males/females*40segs</td>
    </tr>
    <tr>
        <td>ubm</td>
        <td>1-50 *20segs *4</td>
    </tr>
    <tr>
        <td colspan="2">--------------------training set1-------------------</td>
    </tr>
    <tr>
        <td>i-vector</td>
        <td>1-50 *20segs *4</td>
    </tr>
    <tr>
        <td>plda</td>
        <td>1-50 *20segs *4</td>
    </tr>
    <tr>
        <td colspan="2">--------------------training set2-------------------</td>
    </tr>
    <tr>
        <td>i-vector</td>
        <td>50-75 *20segs *4</td>
    </tr>
    <tr>
        <td>plda</td>
        <td>75-100 *20segs *4</td>
    </tr>
    <tr>
        <td colspan="2">-----------------------test set-----------------------</td>
    </tr>
    <tr>
        <td>enroll</td>
        <td>10 *3segs *4</td>
    </tr>
    <tr>
        <td>test</td>
        <td>20 *20segs *4</td>
    </tr>
</table>

#### Reference 
- [Front-End Factor Analysis for Speaker Verification](https://wiki.inf.ed.ac.uk/twiki/pub/CSTR/ListenSemester2201112/dehak-aslp11-front_end_fa.pdf)    
i-vector经典

- [A Straightforward and Efficient Implementation of the Factor Analysis Model for Speaker Verification](http://mistral.univ-avignon.fr/doc/publis/07_Interspeech_Matrouf.pdf)    
训练算法

- [A Small Footprint i-Vector Extractor](https://www.isca-speech.org/archive/odyssey_2012/papers/od12_001.pdf)   

- [Probabilistic Linear Discriminant Analysis for Inferences About Identity](https://wiki.inf.ed.ac.uk/twiki/pub/CSTR/ListenSemester2201112/prince-iccv07-plda.pdf)  
PLDA理论

- [Analysis of I-vector Length Normalization in Speaker Recognition Systems](https://isca-speech.org/archive/archive_papers/interspeech_2011/i11_0249.pdf)  
PLDA打分识别

- [Daniel Garcia-Romero]()  

#### Next
Forced Alignment!!!(音素识别、音节切分, youtu-vector基础)  

1. cmusphinx 加大训练数据量(数据待获取)
2. kaldi [参考实现](https://www.eleanorchodroff.com/tutorial/kaldi/forced-alignment.html)
3. pykaldi 备选
4. 其他实现参考 [forced-alignment-tools](https://github.com/pettarin/forced-alignment-tools)
