## GMM-UBM
-initialisation: 
    -->load all datasets 
    -->pre-processing (front-end of speaker identification)

-creating GMM, UBM and adapted GMM-UBM 
    -->create plain GMM models 
    -->plot number of GMM components against performance 
    -->create UBM 
    -->adapt UBM with MAP estimation and training data

-speaker identification 
    -->create confusion matrices for speaker identification 
    -->for GMM 
    -->for GMM-UBM

-speaker verification 
    -->set thresholds according to training data and ubm data 
    -->conduct impostor trials 
    -->plot FAR, FRR and confusion matrices