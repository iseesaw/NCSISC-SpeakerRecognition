### gmm-ubm + i-vector + plda

#### gmm-ubm
Steps:  
1. 背景数据 -> UBM -> ubm's mean super-vector
2. UBM -> 说话人多条注册语音 -> MAP Adaptation -> 说话人相关GMM
3. 说话人相关GMM -> GMM super-vector(均值超矢量)

Usage:  
说话人测试语音 -> 说话人相关GMM score -> 阈值判断

#### i-vector

给定说话人一段语音, 与之对应的高斯均值超矢量定义为: 
$$s = m + T\omega$$
其中:   

- s (super-vector)
    + 给定说话人语音的高斯均值超矢量(用户相关GMM获得)
- m (ubm's mean super-vector)
    + 通用背景模型(UBM)的高斯均值超矢量(与具体说话人及信道无关)
- T (total-vavriability matrix)
    + 全局差异空间矩阵
- $\omega$ (i-vector)
    + 全局差异空间因子

求解过程:  

- 全局差异空间矩阵T的估计
    + 假设每一段语音都来自不同的说话人
    + 计算训练数据库中每个说话人对应的Baum-Welcn统计量
    + EM算法迭代估计T矩阵(大概10次)
- i-vector提取
    + 计算数据库中每个目标说话人对应的Baum-Welch统计量
    + 带入全局差异空间矩阵T
    + 计算$\omega$的后验均值即为i-vector


#### plda
i-vector包含说话人和信道的信息, 可以使用lda/plda减弱信道的影响

$$X_{ij} = \mu + Fh_{i} + Gw_{ij} + \epsilon_{ij}$$
其中:  

- $\mu + Fh_{i}$ 信号部分, 描述说话人之间的差异(类间差异)
    + $\mu$ 全体训练数据的均值
    + F 身份空间, 包含用来表示各种说话人的信息
    + $h_{i}$ 具体的一个说话人的身份(说话人在身份空间中的位置)
- $Gw_{ij} + \epsilon_{ij}$ 噪音部分, 描述同一说话人的不同语音之间的差异(类内差异)
    + G 误差空间, 包含可以用来表示同一说话人不同语音变化的信息
    + $w_{ij}$ 表示说话人的某一条语音在G空间中的位置
    + $\epsilon_{ij}$ 最后的残留噪声项, 表示尚未解释的东西

用两个假象变量($\theta$, $\Sigma$)描述一个语音的数据结构:  
$$\theta = [\mu, F, G, \Sigma]$$

**plda模型训练**  
目标就是输入一堆数据$X_{ij}$(多个说话人多条语音), 使用EM迭代求解  

- 均值处理
    + 计算所有训练数据$X_{ij}$的均值$\mu$, 从训练数据中减去该均值$X_{ij} = X_{ij} - \mu$
    + 根据训练数据中的人数N, 计算N个人的均值$N_{\mu}$
- 初始化
    + 噪声空间G, 随机初始化
    + 身份空间F, 对每个人的均值数据$N_{\mu}$进行PCA降维, 赋值给F
    + 方差$\Sigma$初始化为常量
- EM迭代优化

**简化版plda**
$$X_{ij} = \mu + Fh{i} + \epsilon_{ij}$$
