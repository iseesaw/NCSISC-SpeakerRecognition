## ASV

## Replay Defender Part

### about MFCC_GMM

* target: used as base line for defending replay attack

* data set: get the data set from the website: https://datashare.is.ed.ac.uk/handle/10283/3055, you should at least download **Training set of the ASVspoof 2017 database** and **Development set of the ASVspoof 2017 database and related protocol_V2**. The structure of the dir should be like this:

  ​	+--------------ASV

  ​		+-----------MFCC_GMM

  ​		+-----------ASVspoof2017_V2

  ​			|-----------ASVspoof2017_V2_train

  ​			|-----------ASVspoof2017_V2_dev

  ​			+-----------protocol_V2

* reference: https://github.com/azraelkuan/asvspoof2017, this project includes ASV tech for CQCC_GMM, MFCC_GMM and DNN method

*  performance: 

  EER = 20.32%

  cost time approximately 5500s



### about CIMFCC_GMM

* reference: 徐涌钞. 基于高频特瓶颈特征的说话人验证系统重放共计检测方法. 哈尔滨工业大学. 2018年6月

* Performance:

  (first version)

  * EER = 15.68 % 
  * cost time approximately  850s



## about GMM_UBM

* target: used as baseline for speaker recognition

* dataset: get the data from the website: https://www.dropbox.com/s/87v8jxxu9tvbkns/development_set.zip?dl=0, then use **data_preprocessing.py** to translate the data set to the form which sidekit package can use. The file structure should be like this:

    +-------------------ASV

      ​	+-------------------GMM_UBM

      		+-------------------development_set

      		+-------------------TI_dataset

      		|-------------------data_preprocessing.py

      		|-------------------main.py

* feature: This part use the same feature as MFCC_GMM does

* reference: http://www-lium.univ-lemans.fr/sidekit/tutorial/rsr2015_gmm_ubm.html, this is the official document of sidekit, teaching you how to run a gmm_ubm and etc.

* performance:
  ​       EER = 29.92%， the official doc gives EER = 41.6% ( In RSR2015 dataset )

  ​	without Voice activity detection, EER = 24.6%

  ​       cost time approximately 1500s

* Attention: 

  ​	the sidekit package in PyPI not work in this project, because windows does not have fork in UNIX, 

  so we change it to single process.