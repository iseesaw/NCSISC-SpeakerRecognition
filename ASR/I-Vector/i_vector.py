# -*- coding: utf-8 -*-
'''
Run a i-vector system
'''
import sidekit
from sidekit import sidekit_io
import numpy as np
import copy

# number of Gaussian distributions for each GMM
distrib_nb = 512
# rank of the total variability matrix
rank_TV = 400
# number of iterations to run
tv_iteration = 10
# rank of the PLDA eigenovoice matrix
plda_rk = 400
feature_dir = ''
feature_extension = ''
nbThread = 10


def ivector():
    ############# 文件读取 ###############
    # 训练UBM
    with open('task/ubm.list', 'r') as f:
       ubm_list = np.array(f.read().split('\n'))
    # ????? IdMap: 训练 Total Variablity Matrix
    tv_idmap = sidekit.IdMap('task/ivector_idmap.h5')
    # ????? IdMap: 训练 PLDA, WCCN, Mahalanobis matrices
    plda_male_idmap = sidekit.IdMap('task/plda_idmap.h5')
    # IdMap: 注册数据
    enroll_idmap = sidekit.IdMap('task/enroll_idmap.h5')
    # IdMap: 登录测试数据
    test_idmap = sidekit.IdMap('task/test_idmap.h5')

    # 计算测试数据score和eer
    test_ndx = sidekit.Ndx('task/test_ndx.h5')
    keys = sidekit.Key('task/test_key.h5')
    ################# End ###############

    # FeaturesServer(已经提取过特征)
    fs = sidekit.FeaturesServer(
        feature_filename_structure='features_cd/train/{}.h5',
        dataset_list=['cep'],
        mask='[0-12]',
        feat_norm='cmvn',
        keep_all_features=False,
        delta=True,
        double_delta=True,
        rasta=True,
        context=None
    )

    # 训练UBM
    ubm = sidekit.Mixture()
    llk = ubm.EM_split(
        fs,
        ubm_list,
        distrib_nb,
        save_partial=False
    )
    ubm.write('data/ubm.h5')
    #ubm.read('data/ubm.h5')

    # 为注册数据创建StateServers对象
    enroll_stat = sidekit.StatServer(enroll_idmap, ubm)
    enroll_stat.accumulate_stat(
        ubm=ubm,
        feature_server=fs,
        seg_indices=range(enroll_stat.segset.shape[0])
    )
    enroll_stat.write('data/enroll_stat.h5')

    # 为测试数据从创建StatServer对象
    test_stat = sidekit.StatServer(test_idmap, ubm)
    test_stat.accumulate_stat(
        ubm=ubm,
        feature_server=fs,
        seg_indices=range(test_stat.segset.shape[0])
    )
    test_stat.write('data/test_stat.h5')

    # 为back数据创建StatServer
    back_idmap = plda_male_idmap.merge(tv_idmap)
    back_stat = sidekit.StatServer(back_idmap, ubm)
    back_stat.accumulate_stat(
        ubm=ubm,
        feature_server=fs,
        seg_indices=range(back_stat.segset.shape[0])
    )
    back_stat.write('data/back_stat.h5')

    # 训练Total Variablity Matrix
    tv_stat = sidekit.StatServer.read_subset('data/back_stat.h5', tv_idmap)
    tv_mean, tv, _, __, tv_sigma = tv_stat.factor_analysis(
        rank_f=rank_TV,
        rank_g=0,
        rank_h=None,
        re_estimate_residual=False,
        it_nb=(tv_iteration, 0, 0),
        min_div=True,
        ubm=ubm,
        batch_size=100,
        save_partial=False
    )
    sidekit_io.write_tv_hdf5(
        (tv, tv_mean, tv_sigma),
        'data/tv_info.h5'
    )

    # 提取注册数据、测试数据、plda数据i-vector
    enroll_stat = sidekit.StatServer('data/enroll_stat.h5')
    enroll_iv = enroll_stat.estimate_hidden(
        tv_mean,
        tv_sigma,
        V=tv,
        batch_size=100
    )[0]
    enroll_iv.write('data/enroll_iv.h5')

    test_stat = sidekit.StatServer('data/test_stat.h5')
    test_iv = test_stat.estimate_hidden(
        tv_mean,
        tv_sigma,
        V=tv,
        batch_size=100
    )[0]
    test_iv.write('data/test_iv.h5')

    plda_stat = sidekit.StatServer.read_subset('data/back_stat.h5', plda_male_idmap)
    plda_iv = plda_stat.estimate_hidden(
        tv_mean,
        tv_sigma,
        V=tv,
        batch_size=100
    )[0]
    plda_iv.write('data/plda_iv.h5')


    enroll_iv = sidekit.StatServer('data/enroll_iv.h5')
    test_iv = sidekit.StatServer('data/test_iv.h5')
    plda_iv = sidekit.StatServer.read_subset('data/plda_iv.h5', plda_male_idmap)

    ###### Begin Using Mahalanobis distance #######
    # meanEFR, CovEFR = plda_iv.estimate_spectral_norm_stat1(3)

    # plda_iv_efr1 = copy.deepcopy(plda_iv)
    # enroll_iv_efr1 = copy.deepcopy(enroll_iv)
    # test_iv_efr1 = copy.deepcopy(test_iv)

    # plda_iv_efr1.spectral_norm_stat1(meanEFR[:1], CovEFR[:1])
    # enroll_iv_efr1.spectral_norm_stat1(meanEFR[:1], CovEFR[:1])
    # test_iv_efr1.spectral_norm_stat1(meanEFR[:1], CovEFR[:1])
    # M1 = plda_iv_efr1.get_mahalanobis_matrix_stat1()
    # scores_mah_efr1 = sidekit.iv_scoring.mahalanobis_scoring(enroll_iv_efr1, test_iv_efr1, test_ndx, M1)
    ######## End Using Mahalanobis distance #######

    ##### Begin Using Two-covariance scoring ######
    # meanSN, CovSN = plda_iv.estimate_spectral_norm_stat1(1, 'sphNorm')
    # plda_iv_sn1 = copy.deepcopy(plda_iv)
    # enroll_iv_sn1 = copy.deepcopy(enroll_iv)
    # test_iv_sn1 = copy.deepcopy(test_iv)

    # plda_iv_sn1.spectral_norm_stat1(meanSN[:1], CovSN[:1])
    # enroll_iv_sn1.spectral_norm_stat1(meanSN[:1], CovSN[:1])
    # test_iv_sn1.spectral_norm_stat1(meanSN[:1], CovSN[:1])

    # W = plda_iv_sn1.get_within_covariance_stat1()
    # B = plda_iv_sn1.get_between_covariance_stat1()
    # scores_2cov_sn1 = sidekit.iv_scoring.two_covariance_scoring(
    #     enroll_iv_sn1,
    #     test_iv_sn1,
    #     test_ndx,
    #     W,
    #     B
    # )
    ###### End Using Two-covariance scoring #######

    ############## Begin Using PLDA ###############
    # 使用plda_iv训练plda
    meanSN, CovSN = plda_iv.estimate_spectral_norm_stat1(1, 'sphNorm')

    plda_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])
    enroll_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])
    test_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])
    plda_mean, plda_F, plda_G, plda_H, plda_Sigma = plda_iv.factor_analysis(
        rank_f=plda_rk,
        rank_g=0,
        rank_h=None,
        re_estimate_residual=True,
        it_nb=(10, 0, 0),
        min_div=True,
        ubm=None,
        batch_size=1000
    )
    sidekit_io.write_plda_hdf5(
        (plda_mean, plda_F, plda_G, plda_Sigma),
        'data/plda_info.h5'
    )

    # 注册、登录评分
    scores_plda = sidekit.iv_scoring.PLDA_scoring(
        enroll_iv, # 注册数据i-vector
        test_iv, # 测试数据i-vector
        test_ndx, # 测试数据segment-model表
        ### plda训练参数 ###
        plda_mean,
        plda_F,
        plda_G,
        plda_Sigma,
        full_model=False
    )
    scores_plda.write('data/scores_plda.h5')
    ################ End Using PLDA ###############

    print(np.max(scores_plda.scoremat, axis=0))
    print(np.argmax(scores_plda.scoremat, axis=0))
    # > 0.5 True else False
    # n = 0
    # threshold = 3
    # tp, fp, tn, fn = 0, 0, 0, 0
    # for i, m in enumerate(np.max(scores_plda.scoremat, axis=0)):
    #     if i < 20 and m > threshold:
    #         n += 1
    #         tp += 1
    #     if i > 20 and m < threshold:
    #         n += 1
    #         tn += 1
    #     if i < 20 and m < threshold:
    #         fn += 1
    #     if i > 20 and m > threshold:
    #         fp += 1
    # p = tp / (tp + fp)
    # r = tp / (tp + fn)
    # print('accur {}\nprecion {}\nrecall {}\nf1 {}'.format(n / 40, p, r, 2 *
    #                                                       p * r / (p + r)))
    # # Set the prior following NIST-SRE 2008 settings
    prior = sidekit.logit_effective_prior(0.01, 10, 1)
    # Initialize the DET plot to 2008 settings
    dp = sidekit.DetPlot(window_style='cross device', plot_title='i-vector')
    dp.set_system_from_scores(scores_plda, test_key, sys_name='i-vector')
    # dp.create_figure()
    # dp.plot_rocch_det(0)
    # dp.plot_DR30_both(idx=0)
    # dp.plot_mindcf_point(prior, idx=0)
    minDCF, Pmiss, Pfa, prbep, eer = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[0], dp.__non__[0], prior, normalize=True)
    print("i-vector, minDCF = {}, eer = {}".format(minDCF, eer))


if __name__ == '__main__':
    ivector()
