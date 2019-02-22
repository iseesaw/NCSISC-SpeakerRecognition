import numpy as np
import os
import sys
import multiprocessing
import matplotlib.pyplot as mpl
import logging
import sidekit

#logging.basicConfig(filename='log/ubm-gmm.log', level=logging.DEBUG)

distribNum = 64  # number of Gaussian distributions for each GMM
dataBasePath = './TI_dataset'

protocolPath = os.path.join(dataBasePath, 'protocol')  # protocol specify the info about data

# Automatically set the number of parallel process to run
threadNum = multiprocessing.cpu_count()


if __name__ == '__main__':
    multiprocessing.freeze_support()

    # load task definition
    print('Load task definition...')
    enroll_idmap = sidekit.IdMap.read_txt(os.path.join(protocolPath, 'enroll.txt'))
    test_ndx = sidekit.Ndx.read_txt(os.path.join(protocolPath, 'test.txt'))
    key = sidekit.Key.read_txt(os.path.join(protocolPath, 'label.txt'))
    ubmList = []
    with open(os.path.join(protocolPath, 'total.txt'), 'r') as f:
        for line in f:
            ubmList.append(line.strip())


    # Process the audio to extract MFCC
    print('Init FeaturesExtractor')
    extractor = sidekit.FeaturesExtractor(audio_filename_structure=dataBasePath+'/{}.wav', 
        feature_filename_structure='./feature/{}.h5', sampling_frequency=16000, lower_frequency=133.33,
        higher_frequency=6955.50, filter_bank='log', filter_bank_size=40, window_size=0.025, shift=0.01, ceps_number=19,
        vad='snr', snr=40, pre_emphasis=0.97, save_param=['vad', 'energy', 'cep'], keep_all_features=False)

    # get the complete list of features to extract 
    show_list = np.unique(ubmList)

    channel_list = np.zeros_like(show_list, dtype=int)

    print('Extract features and save to disk')
    extractor.save_list(show_list=show_list, channel_list=channel_list, num_thread=1)

    # Create a FeaturesServer to load features and feed the other methods
    features_server = sidekit.FeaturesServer(features_extractor=None, feature_filename_structure='./feature/{}.h5',
        sources=None, dataset_list=['energy', 'cep', 'vad'], mask=None, feat_norm='cmvn', global_cmvn=None, dct_pca=False, 
        dct_pca_config=None, sdc=False, sdc_config=None, delta=True, double_delta=True, delta_filter=None, context=None, traps_dct_nb=None, 
        rasta=True, keep_all_features=False)

    print('Train the UBM by EM')
    # Extract all features and train a GMM without writing to disk
    ubm = sidekit.Mixture()
    llk = ubm.EM_split(features_server, ubmList, distribNum, num_thread=1, save_partial=True)
    ubm.write('gmm/ubm.h5')

    print('Compute the sufficient statistics')
    # Create a StatServer for the enrollment data and compute the statistics 
    enroll_stat = sidekit.StatServer(enroll_idmap, distribNum, feature_size=60)
    enroll_stat.accumulate_stat(ubm=ubm, feature_server=features_server, seg_indices=range(enroll_stat.segset.shape[0]), 
        num_thread=1)
    enroll_stat.write('data/stat_enroll.h5')

    print('MAP adaptation of the speaker models')
    regulation_factor = 3 
    enroll_sv = enroll_stat.adapt_mean_map_multisession(ubm, regulation_factor)
    enroll_sv.write('data/sv_enroll.h5')

    print('Compute trial scores')
    scores_gmm_ubm = sidekit.gmm_scoring(ubm, enroll_sv, test_ndx, features_server, 
        num_thread=1)
    scores_gmm_ubm.write('scores/scores_gmm_ubm.h5')

    # Compute EER
    print('Plot the DET curve')
    prior = sidekit.logit_effective_prior(0.001, 1, 1)
    dp = sidekit.DetPlot(window_style='sre10', plot_title='GMM-UBM')
    dp.set_system_from_scores(scores_gmm_ubm, key, sys_name='GMM-UBM')   
    minDCF, Pmiss, Pfa, prbep, eer = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[0], dp.__non__[0], prior, normalize=True)
    print('EER = {}'.format(eer)) 






