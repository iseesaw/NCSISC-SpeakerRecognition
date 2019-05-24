import librosa
import numpy as np
from scipy.spatial import distance


def pearson_scoring(first, second):
    """

    :param first: n_samples x n_features
    :param second: n_samples x n_features
    :return:
    """
    cor = np.corrcoef(first, second, rowvar=False)
    return np.average(cor)


def dtw_scoring(first, second, dist_metric='cosine'):
    """

    :param first:
    :param second:
    :param dist_metric:
    :return:
    """
    d, wp = librosa.core.dtw(first, second, metric=dist_metric)
    return d[d.shape[0]-1][d.shape[1]-1]


def cosine_scoring(first, second):
    """

    :param first:
    :param second:
    :return:
    """
    f = first.T
    s = second.T
    cos = []
    for i in range(f.shape[0]):
        cos.append(1 - distance.cosine(f[i], s[i]))
    return np.average(cos)


def cosine_variance_scoring(first, second):
    """

    :param first:
    :param second:
    :return:
    """
    f = first.T
    s = second.T
    cos = []
    for i in range(f.shape[0]):
        cos.append(1 - distance.cosine(f[i], s[i]))
    return np.average(cos), np.std(cos)




def pearson_cosine_fusion_scoring(first, second):
    """
    :param first:
    :param second:
    :return:
    """
    c_s = (cosine_scoring(first, second) - 0.5) * 2
    p_s = pearson_scoring(first, second)
    return 0.6 * c_s + 0.4 * p_s


def p_c_fusion_scoring(first, second):
    """

    :param first:
    :param second:
    :return:
    """
    f = first.T
    s = second.T
    cos = []
    for i in range(f.shape[0]):
        cos.append(1 - distance.cosine(f[i], s[i]))

    cor = np.corrcoef(first, second, rowvar=False)

    return 0.7 * np.average(cos) + 0.3 * np.nanmean(cor), 0.7 * np.std(cos) + 0.3 * np.nanstd(cor)