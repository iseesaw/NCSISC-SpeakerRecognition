**By. Zhang Kaiyan**  

>该文件夹下为声纹识别(Speaker Recognition)相关资料及代码实现  

### 文本相关(Text-Dependent)的声纹识别  

**注册**： 用户关于某一文本内容( :bulb: 数字串、短语串、英文/中文)的语音录入多次, 作为样本  
**登录**： 用户关于某一文本内容的语音  

### 相关模型
| 模型 | 相关描述 | 完成度 |
| --- | --- | --- |
| MFCC-DTW | 最简单的模型, 计算注册语音与登录语音MFCC特征向量的距离, 设置阈值进行判断 | 待验证 |
| GMM-UBM | 通常作为基线模型, 注册时需要重复录入语音 |  待验证 |
| i-vector | UBM-ivector-PLDA/SVM | 待完善 |
| End2End | 语音直接作为LSTM/RNN输入；训练embedding；CNN判别模型 | 待实现 |


### 文件结构
 - Database 说话人识别数据集(数据保存本地, 上传README)
 - End2End 端到端模型相关
 - GMM_UBM GMM-UBM模型实现相关代码
 - MFCC_DTW MFCC-DTW实现相关代码
 - Refs 相关模型参考文件
 - SIDEKIT sidekit包使用及相关模型实现