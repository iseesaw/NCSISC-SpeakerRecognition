### Kaldi sre16 Model
使用Kaldi sre16预训练模型提取x-vector并进行后续的plda训练和评分  
Ref: [ivector-xvector](https://github.com/zeroQiaoba/ivector-xvector#other-summary)  

大致按照GitHub的README进行  
- 几个注意点
    + 采样率要在config/mfcc中设置, 以及添加允许重采样
    + speaker.txt格式为```uttr_path speaker_id```(./wav/audio1.wav speaker1)
    + 将特征文件转为txt并读取进行后端判断(cosin、plda)

初步得分0.57-0.64

- next
    + 后端使用plda, Ref [FactoryAnalyser](https://projets-lium.univ-lemans.fr/sidekit/_modules/factor_analyser.html#FactorAnalyser.plda) [PLDA_scoring](https://projets-lium.univ-lemans.fr/sidekit/_modules/iv_scoring.html#full_PLDA_scoring)
    + 看run.sh源码, 尝试重训练x-vector网络、以及run.pl中代码、尝试plda训练