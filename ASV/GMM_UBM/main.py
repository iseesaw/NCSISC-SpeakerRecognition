import sidekit
import os
import sys
import multiprocessing
import matplotlib.pyplot as mpl
import logging
import numpy as np

distribNum = 64  # number of Gaussian distributions for each GMM
dataBasePath = './TI_dataset'

protocolPath = os.path.join(dataBasePath, 'protocol')  # protocol specify the info about data

# Automatically set the number of parallel process to run
threadNum = 1

if __name__ == '__main__':
    print('Load task definition...')
    enroll_idmap = sidekit.IdMap.read_txt(os.path.join(protocolPath, 'enroll.txt'))
    test_ndx = sidekit.Ndx.read_txt(os.path.join(protocolPath, 'test.txt'))
    test_key = sidekit.Key.read_txt(os.path.join(protocolPath, 'label.txt'))
    ubmList = []
    with open(os.path.join(protocolPath, 'total.txt')) as f:
        for line in f:
            ubmList.append(line.rstrip())


    print('Extract MFCC features...')
    extractor = sidekit.FeaturesExtractor(audio_filename_structure=dataBasePath+"/{}.wav",
                                          feature_filename_structure="./features/{}.h5",
                                          sampling_frequency=16000,
                                          lower_frequency=133.3333,
                                          higher_frequency=6955.4976,
                                          filter_bank="log",
                                          filter_bank_size=40,
                                          window_size=0.025,
                                          shift=0.01,
                                          ceps_number=19,
                                          vad=None,
                                          pre_emphasis=0.97,
                                          save_param=["energy", "cep"],
                                          keep_all_features=True)

    show_list = np.unique(ubmList)
    channel_list = np.zeros_like(show_list, dtype = int)

    # Get the complete list of features to extract
    show_list = np.unique(ubmList)
    channel_list = np.zeros_like(show_list, dtype = int)

    extractor.save_list(show_list=show_list,
                        channel_list=channel_list,
                        num_thread=threadNum)


    # Create a FeaturesServer to load features and feed the other methods
    features_server = sidekit.FeaturesServer(features_extractor=None,
                                             feature_filename_structure="./features/{}.h5",
                                             sources=None,
                                             dataset_list=["energy", "cep", "vad"],
                                             mask=None,
                                             feat_norm="cmvn",
                                             global_cmvn=None,
                                             dct_pca=False,
                                             dct_pca_config=None,
                                             sdc=False,
                                             sdc_config=None,
                                             delta=True,
                                             double_delta=True,
                                             delta_filter=None,
                                             context=None,
                                             traps_dct_nb=None,
                                             rasta=True,
                                             keep_all_features=False)


    print('Train the UBM by EM')
    # Extract all features and train a GMM without writing to disk
    ubm = sidekit.Mixture()
    llk = ubm.EM_split(features_server, ubmList, distribNum, num_thread=threadNum, save_partial=True)
    ubm.write('gmm/ubm.h5')
    ubm.read('gmm/ubm.h5')

    print('Compute the sufficient statistics')
    # Create a StatServer for the enrollment data and compute the statistics
    enroll_stat = sidekit.StatServer(enroll_idmap,
                                     distrib_nb=64,
                                     feature_size=60)
    enroll_stat.accumulate_stat(ubm=ubm,
                                feature_server=features_server,
                                seg_indices=range(enroll_stat.segset.shape[0]),
                                num_thread=threadNum)
    enroll_stat.write('data/stat_enroll.h5')

    print('MAP adaptation of the speaker models')
    regulation_factor = 3  # MAP regulation factor
    enroll_sv = enroll_stat.adapt_mean_map_multisession(ubm, regulation_factor)
    enroll_sv.write('data/sv_enroll.h5')


    print('Compute trial scores')
    scores_gmm_ubm = sidekit.gmm_scoring(ubm,
                                         enroll_sv,
                                         test_ndx,
                                         features_server,
                                         num_thread=threadNum)
    scores_gmm_ubm.write('scores/scores_gmm-ubm.h5')


    print('Plot the DET curve')
    # Set the prior following NIST-SRE 2008 settings
    prior = sidekit.logit_effective_prior(0.01, 10, 1)

    # Initialize the DET plot to 2008 settings
    dp = sidekit.DetPlot(window_style='sre10', plot_title='GMM-UBM')
    dp.set_system_from_scores(scores_gmm_ubm, test_key, sys_name='GMM-UBM')
    dp.create_figure()
    dp.plot_rocch_det(0)
    dp.plot_DR30_both(idx=0)
    dp.plot_mindcf_point(prior, idx=0)
    minDCF, Pmiss, Pfa, prbep, eer = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[0], dp.__non__[0], prior, normalize=True)
    print("UBM-GMM, minDCF = {}, eer = {}".format(minDCF, eer))