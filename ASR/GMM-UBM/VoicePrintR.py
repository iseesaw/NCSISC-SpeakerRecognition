# -*- coding: utf-8 -*-
'''
FeaturesExtractor() --> features_extractor
FeaturesServer() --> features_server
Mixture() --> ubm -> read()
StatServer() --> enroll_stat -> accumulate_stat() -> adapt_mean_map_multisession ->enroll_sv
gmm_scoring() <-- ubm, enroll_sv, test_ndx, features_server
--> scores_gmm_ubm.scoremat
'''
import numpy as np
import sidekit
import time
import sys
import warnings
from config import *
warnings.filterwarnings('ignore')


class VPR():

    def __init__(self):
        self.distribNb = 512
        self.utils()

    def utils(self):
        '''
        Create Objects
        :return: features_extractor, features_server, ugm
        '''
        self.features_extractor = sidekit.FeaturesExtractor(
            audio_filename_structure=data_path + '{}.wav',
            feature_filename_structure=dir_path + 'userdata\\{}.h5',
            sampling_frequency=16000,
            lower_frequency=133.3333,
            higher_frequency=6955.4976,
            filter_bank='log',
            filter_bank_size=40,
            window_size=0.025,
            shift=0.01,
            ceps_number=20,
            vad='snr',
            snr=40,
            pre_emphasis=0.97,
            save_param=['cep'],  # 'vad', 'energy',
            keep_all_features=False
        )

        self.features_server = sidekit.FeaturesServer(
            features_extractor=None,
            feature_filename_structure=dir_path + 'userdata\\{}.h5',
            sources=None,
            dataset_list=['cep'],
            mask=None,
            feat_norm='cmvn',
            global_cmvn=None,
            dct_pca=False,
            dct_pca_config=None,
            sdc=False,
            sdc_config=None,
            ###
            delta=True,
            double_delta=True,
            ###
            delta_filter=None,
            context=None,
            traps_dct_nb=None,
            rasta=True,
            keep_all_features=False
        )

        self.ubm = sidekit.Mixture()

        self.ubm.read(dir_path + 'model\\ubm_King_all.h5')

    def delete_f(file):
        file = dir_path + '\\userdata\\{}.h5'.format(file)
        if os.path.exists(file):
            os.path.remove(file)

    def enroll(self, user):
        '''
        User Enroll --> enroll_idmap
        :param user, the person to enroll
        :return: enroll_stat, enroll_sv
        '''
        # enroll data
        models = []
        segments = []
        enrollN = 3
        for i in range(enrollN):
            models.append(user)
            segment = enroll_f.format(username=user, index=i + 1)
            segments.append(segment)
            self.delete_f(segment)
        enroll_idmap = sidekit.IdMap()
        enroll_idmap.leftids = np.asarray(models)
        enroll_idmap.rightids = np.asarray(segments)
        enroll_idmap.start = np.empty(enroll_idmap.rightids.shape, '|O')
        enroll_idmap.stop = np.empty(enroll_idmap.rightids.shape, '|O')
        #enroll_idmap.write(dir_path + 'userdata\\{}_enroll_idmap.h5'.format(user))

        ############# features_extractor ############
        show_list = np.unique(enroll_idmap.rightids)
        channel_list = np.zeros_like(show_list, dtype=int)
        self.features_extractor.save_list(
            show_list=show_list,
            channel_list=channel_list,
        )
        #############################################

        enroll_stat = sidekit.StatServer(
            enroll_idmap,
            distrib_nb=self.distribNb,
            feature_size=60
        )

        # caculate stat0 stat1
        enroll_stat.accumulate_stat(
            ubm=self.ubm,
            feature_server=self.features_server,
            seg_indices=range(enroll_stat.segset.shape[0])
        )
        # enroll_stat.write(
        #     dir_path + 'userdata\\{}_enroll_stat.h5'.format(user))

        # train gmm super-vector
        regulation_factor = 3
        enroll_sv = enroll_stat.adapt_mean_map_multisession(
            self.ubm, regulation_factor)
        self.delete_f('{}_enroll_sv'.format(user))
        enroll_sv.write()

    def login(self, user, path):
        '''
        User Login --> test_ndx
        :return: scores
        '''
        # test_data
        models = [user]
        segments = [path]
        test_ndx = sidekit.Ndx()
        test_ndx.modelset = np.asarray(models)
        test_ndx.segset = np.asarray(segments)
        test_ndx.trialmask = np.ones((1, 1), dtype='bool')
        ########### extract features ############
        self.delete_f(path)
        show_list = np.unique(test_ndx.segset)
        channel_list = np.zeros_like(show_list, dtype=int)
        self.features_extractor.save_list(
            show_list=show_list,
            channel_list=channel_list,
            # num_thread=nbThread
        )
        ##########################################

        # read enroll_sv
        sv_path = dir_path + 'userdata\\{}_enroll_sv.h5'.format(user)
        sv = sidekit.StatServer(sv_path)
        self.delete_f('{}_enroll_sv'.format(user))
        # score
        scores_gmm_ubm = sidekit.gmm_scoring(
            self.ubm,
            sv,
            test_ndx,
            self.features_server
        )
        return 'yes' if scores_gmm_ubm.scoremat[0][0] > 1.1 else 'no', scores_gmm_ubm.scoremat[0][0]


if __name__ == '__main__':

    vpr = VPR()
    vpr.enroll('zky')
    # if sys.argv[1] == 'enroll':
    #     try:
    #         vpr.enroll(sys.argv[2])
    #         print('yes')
    #     except:
    #         print('no')
    # if sys.argv[1] == 'login':
    #     try:
    #         result, score = vpr.login(sys.argv[2], sys.argv[3])
    #         print(result)
    #         print('{:.2f}'.format(score))
    #     except:
    #         print('no')
