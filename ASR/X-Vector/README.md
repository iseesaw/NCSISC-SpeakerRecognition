## 挑战杯-跨设备说话人识别
i-vector/x-vector + plda   
主要从~~代码实现和~~Kaldi模型~~实现两个方面~~进行  

### ~~x-vector代码实现~~
~~步骤参考[tdnn.md](tdnn.md)  
Demo代码[x_vector.py](x_vector.py) ~~

### Kaldi模型
自己训练或者用已经有的, 考虑到训练数据规模的问题 

#### 训练模型Kaldi模型步骤
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

#### 使用Kaldi已有模型
- [使用sre16预训练模型提取x-vector](kaldi_xvector.md)  
    + 参考[x-vector/README](x-vector/README.md)
- [sre16/v2](https://github.com/kaldi-asr/kaldi/tree/master/egs/sre16/v2)  
- [voxceleb/v2](https://github.com/kaldi-asr/kaldi/tree/master/egs/voxceleb/v2)  									

### 测试集A得分情况
$$Score = \frac{\Sigma_{i}^{N}{\beta{(p_i)}}}{N}$$
$$\beta{(p_i)}当且仅当p_i为真时等于1, 否则等于0; p_i为真当且仅当语音i判断正确$$

<table>
    <tr>
        <td>模型</td>
        <td>
            训练数据及设置<br>
            Aishell(100m 100f) <br>
            ST2017(100m 100f)
        </td>
        <td>六组测试得分</td>
    </tr>
    <tr>
        <td rowspan="3">
            i-vector <br>
            sidekit
        </td>
        <td>
            AIshell + ST2017 s<br>
            ubm 25p *4 *30s <br>
            i-vector 50p *4 *20s<br>
            plda 50p *4 *20s <br>
        </td>
        <td>
            group0 threshold=5/10 score=0.61/0.58 <br>
            group1 threshold=0 score=0.57 <br>
            group2 threshold=5 score=0.56 <br>
            group3 threshold=0 score=0.54 <br>
            group4 threshold=0/5 score=0.65/0.7 <br>
            group5 threshold=-10/25 score=0.56 <br>
        </td>
    </tr>
    <tr>
        <td>
            AIshell<br>
            ubm (100m + 100f)*20s<br>
            i-vector (50m + 50f)*20s<br>
            plda (50m + 50f)*20s
        </td>
        <td>
            group0 threshold=5/15 score=0.61 <br>
            group1 threshold=5 score=0.55 <br>
            group2 threshold=0 score=0.56 <br>
            group3 threshold=5 score=0.54 <br>
            group4 threshold=0/5 score=0.63/0.66 <br>
            group5 threshold=-5 score=0.58 <br>
        </td>
    </tr>
    <tr>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="4">
            x-vector <br>
            Kaldi
        </td>
        <td>
            sre16 model <br>
            backend - cosin
        </td>
        <td>
            group0 threshold=0.5 score=0.64 <br>
            group1 threshold=0.5 score=0.59 <br>
            group2 threshold=0.5 score=0.57 <br>
            group3 threshold=0.5 score=0.61 <br>
            group4 threshold=0.5 score=0.54 <br>
            group5 threshold=0.5 score=0.59 <br>
        </td>
    </tr>
    <tr>
        <td>
            sre16 model <br>
            backend - plda <br>
            sidekit, 100*50uttrs
        </td>
        <td>
            group0 threshold=10-13/35 score=0.67 <br>
            group1 threshold=25 score=0.65 <br>
            group2 threshold=30-34 score=0.74 <br>
            group3 threshold=25-30 score=0.67 <br>
            group4 threshold=20-25 score=0.65 <br>
            group5 threshold=35-40 score=0.57 <br>
        </td>
    </tr>
    <tr>
        <td>
            voxceleb <br>
            backend - plda <br>
            (sidekit)
        </td>
        <td>
            group0 threshold=14-16score=0.7 <br>
            group1 threshold=20-25 score=0.58 <br>
            group2 threshold=18-25 score=0.65 <br>
            group3 threshold=20-25 score=0.73 <br>
            group4 threshold=25-28 score=0.7 <br>
            group5 threshold=21-25 score=0.6 <br>
        </td>
    </tr>
    <tr>
        <td>
            voxceleb <br>
            backend - plda <br>
            (Kaldi)
        </td>
        <td>
            <strong>
            group0 threshold=8-14 score=0.83 <br>
            group1 threshold=8-14 score=0.86 <br>
            group2 threshold=12-16 score=0.79 <br>
            group3 threshold=10-16 score=0.87 <br>
            group4 threshold=8-12 score=0.8 <br>
            group5 threshold=12-16 score=0.78 <br>
            </strong>
        </td>
    </tr>
</table>


#### Next
使用Kaldi的voxveleb模型进行x-vector和plda, 6组平均得分0.82  
下一步可以改进的地方:   

- shell脚本编写
    + 完善测试语音数据切分脚本
    + 编写x-vector extract + plda计算一体化脚本
    + 使用shell + python模式
- 在Kaldi上使用aishell(1, 2)数据(+ST2017)训练x-vector和plda
    + 考虑使用不同信道(IOS、Android、Desktop)的数据训练(3000+speakers, 1000+hours)
    + 使用data argument(要选择好数据)
    + 根据run.sh修改
    + 准备训练数据文件或预提取特征
    + 尝试GPU训练