import sys
import settings
import os
from utils import phomeframe
import numpy as np
from utils import doppler_feature
import settings
import math
from utils import scoring


"""
run command: python3 enroll.py [username] [user_root_path]
assume user_root_path like this:
enroll
|--15545577320
|  |--enroll1.wav
|  |--enroll1.lab
|  |--...
|  ...
|--TextGrid
"""
if __name__ == '__main__':
    username = sys.argv[1]
    user_root_path = sys.argv[2]
    files = os.listdir(user_root_path)
    enroll_pf_list = []
    for file in files:
        if not os.path.isdir(os.path.join(user_root_path, file)):
            splits = file.split('.')
            if splits[1] == 'wav':
                enroll_wav = splits[0]
                pf = phomeframe.PhomeFrame.read_raw(os.path.join(user_root_path, file), os.path.join(user_root_path,
                                                                       os.path.join('../TextGrid',
                                                                                    enroll_wav + '.TextGrid')))
                enroll_pf_list.append(pf)
    pf_length_list = [pf.number_of_frames() for pf in enroll_pf_list]
    pf_length_list = np.array(pf_length_list)
    median = np.median(pf_length_list)
    median_idx = np.argmin(np.abs(median - pf_length_list))
    norm_pf_list = []
    for i in range(len(enroll_pf_list)):
        if not i == median_idx:
            norm_pf_list.append(doppler_feature.length_normalize(enroll_pf_list[i], enroll_pf_list[median_idx]))
        else:
            norm_pf_list.append(enroll_pf_list[i])

    corrected_pf = phomeframe.PhomeFrame()
    corrected_pf.starts = enroll_pf_list[median_idx].starts
    corrected_pf.ends = enroll_pf_list[median_idx].ends
    avg_feats = None
    for pf in norm_pf_list:
        if avg_feats is None:
            avg_feats = pf.feats
        else:
            avg_feats = avg_feats + pf.feats
    avg_feats = avg_feats / len(norm_pf_list)
    corrected_pf.feats = avg_feats
    corrected_pf.write(os.path.join(settings.ENROLL_FEATURE_PATH, username + '.h5'))

    corrected_means = []
    corrected_stds = []

    corrected_pf_one_feats = corrected_pf.get_all_phome_feature_as_one()
    for pf in enroll_pf_list:
        means = []
        stds = []
        normed_pf = doppler_feature.length_normalize(pf, corrected_pf)
        normed_pf_one_feats = normed_pf.get_all_phome_feature_as_one()
        for i in range(normed_pf_one_feats.shape[0]):
            mean, std = scoring.p_c_fusion_scoring(corrected_pf_one_feats[i], normed_pf_one_feats[i])

            if math.isnan(mean) or math.isnan(std):
                means.append(settings.MAX_MEAN_VALUE)
                stds.append(settings.MAX_STD_VALUE)
            else:
                means.append(mean)
                stds.append(std)

        corrected_means.append(np.mean(means))
        corrected_stds.append(np.mean(stds))

    with open(os.path.join(settings.SCORE_PATH, username+'.s'), 'w') as f:
        f.write(str(np.mean(corrected_means)) + ' ' + str(np.mean(corrected_stds)) + '\n')




