from scipy import stats
from utils import phomeframe
import numpy as np
import heapq
from scipy.spatial import distance


def k_closest_neighbours(x, k):
    """

    :param x: n_samples x n_features
    :param k:
    :return:
    """
    heap = []
    for i in range(1, x.shape[0]):
        heapq.heappush(heap, (distance.euclidean(x[i-1], x[i]), i))

    pairs = heapq.nsmallest(k, heap)
    ret = []
    for item in pairs:
        ret.append(item[1])
    return ret


def k_furthest_neighbours(X, k):
    """

    :param X: n_samples x n_features
    :param k: k < n_samples
    :return:
    """
    heap = []
    for i in range(1, X.shape[0]):
        heapq.heappush(heap, (distance.euclidean(X[i-1], X[i]), i))

    pairs = heapq.nlargest(k, heap)
    ret = []
    for item in pairs:
        ret.append(item[1])
    return ret


def k_copy_append(X, k):
    """

    :param X:
    :param k:
    :return:
    """
    ret = []
    if X.shape[0] % 2 == 0:
        left = X.shape[0] // 2 - 1
        right = X.shape[0] // 2
        cnt = 0
        while cnt < k:
            if left < 0:
                left = X.shape[0] // 2 - 1
            ret.append(left)
            cnt = cnt + 1
            left = left - 1
            if cnt >= k:
                break

            if right >= X.shape[0]:
                right = X.shape[0] // 2
            ret.append(right)
            cnt = cnt + 1
            right = right + 1
            if cnt >= k:
                break
    else:
        median = X.shape[0] // 2
        ret.append(median)
        cnt = 1
        left = median - 1
        right = median + 1
        while cnt < k:
            ret.append(left)
            cnt = cnt + 1
            if cnt >= k:
                break
            ret.append(right)
            cnt = cnt + 1
            if cnt >= k:
                break
            left = left - 1
            right = right + 1
            if left < 0:
                left = median - 1
            if right >= X.shape[0]:
                right = median + 1
    ret = list(map(int, ret))
    return ret



def predict_by_k_neighbours(X, pos, k=3):
    """

    :param X: n_samples x n_features nda array
    :param pos: m idx position
    :param k:
    :return:
    """

    gen_X = []

    pos.sort()

    for p in pos:
        sum_neighbours = None
        p_neighbour_idx = [p+i for i in [-2, -1, 0, 1, 2, 3]]
        #print(X.shape[0])
        #print(p_neighbour_idx)
        c = 0
        for idx in p_neighbour_idx:
            if 0 <= idx < X.shape[0]:
                c = c+1
                if sum_neighbours is None:
                    sum_neighbours = X[idx]
                else:
                    sum_neighbours += X[idx]
        x = sum_neighbours / c
        gen_X.append(x)

    ret = []
    cnt = 0
    for i in range(X.shape[0]):
        ret.append(X[i])
        if i in pos:
            appear_cnt = np.sum([e == i for e in pos])
            for c in range(appear_cnt):
                ret.append(gen_X[cnt])
                cnt = cnt+1

    #print('*********')
    #print(X.shape[0])
    #print(pos)
    #print(cnt - len(gen_X))

    return np.array(ret)


def length_normalize(currentpf, targetpf):
    """
    tend to use Cepstrum Length Normalization,
    for current.length < target.length, append new frames by interpolating neighboring
    frames
    for current.length > target.length, delete frames which have minimum distortion to
    their neighbours

    :param currentpf:
    :param targetpf:
    :return:
    """

    # check if they have same segment number
    if not currentpf.starts.shape[0] == targetpf.starts.shape[0]:
        raise Exception('Invalid phomeframe, can not normalize')

    ret_pf = phomeframe.PhomeFrame()
    ret_pf.starts = targetpf.starts
    ret_pf.ends = targetpf.ends

    # normalize each segment
    ret_feats = None
    for idx in range(currentpf.starts.shape[0]):
        cur_seg_len = currentpf.ends[idx] - currentpf.starts[idx]
        tar_seg_len = targetpf.ends[idx] - targetpf.starts[idx]

        pho_frames = currentpf.feats[currentpf.starts[idx]:currentpf.ends[idx]]
        #print('------------------')
        #print(currentpf.starts[idx])
        #print(currentpf.ends[idx])
        #print(currentpf.feats.shape)
        # need to delete frames that represent the steady state of each segment
        if cur_seg_len > tar_seg_len:
            deleteNum = cur_seg_len - tar_seg_len
            deleteIdx = k_closest_neighbours(pho_frames, deleteNum)
            corrected_frames = []
            for frame_seq in range(pho_frames.shape[0]):
                if frame_seq not in deleteIdx:
                    corrected_frames.append(pho_frames[frame_seq])
            corrected_frames = np.array(corrected_frames)

            if ret_feats is None:
                ret_feats = corrected_frames
            else:
                ret_feats = np.concatenate((ret_feats, corrected_frames), axis=0)

        elif cur_seg_len < tar_seg_len:  # need to create frames by band-limited interpolation
            increaseNum = tar_seg_len - cur_seg_len
            #print(pho_frames.shape[0])
            if pho_frames.shape[0] > increaseNum:
                increaseIdx = k_closest_neighbours(pho_frames, increaseNum)
            else:
                increaseIdx = k_copy_append(pho_frames, increaseNum)
                # print(increaseIdx)
            #print(pho_frames.shape[0])
            frames = predict_by_k_neighbours(pho_frames, increaseIdx, k=3)
            if ret_feats is None:
                ret_feats = frames
            else:
                ret_feats = np.concatenate((ret_feats, frames), axis=0)
        else:
            if ret_feats is None:
                ret_feats = pho_frames
            else:
                ret_feats = np.concatenate((ret_feats, pho_frames), axis=0)

        # print(ret_feats[idx].shape == targetpf.feats[idx].shape)

    ret_pf.feats = np.array(ret_feats)
    return ret_pf


def zero_one_normalization(feat):
    max = np.amax(feat)
    min = np.amin(feat)

    feat = (feat - min) / (max - min)
    return feat


def mean_normalization(x):
    """

    :param x: n_samples x n_features nda array
    :return:
    """
    avg = np.average(x, axis=0)
    return x - avg

def zscore_normalization(x):
    """

    :param x:
    :return:
    """
    return stats.zscore(x, axis=0)


def centroid_freq(magnitudes, freq_bin):
    """
    compute the centroid frequency use the formula:
        centroid = $\sum f(n)x(n) / \sum x(n)$

    :param magnitudes:
    :param freq_bin:
    :return:
    """
    magnitudes = np.array(magnitudes)
    freq_bin = np.array(freq_bin)
    freq_bin_idicator = [(1 if e > 0 else 0) for e in freq_bin]
    mag_sum = np.sum(magnitudes*np.array(freq_bin_idicator))
    if mag_sum == 0.0:
        return np.average(freq_bin)
    # for i in range(freq_bin.shape[0]):
    #    if freq_bin[i] > 0:
    #        print(str(magnitudes[i]) + " " + str(freq_bin[i]))
    tmp = np.sum(magnitudes*freq_bin) / mag_sum
    # print(tmp)
    # print('+++++++++++++++++++++=')
    return tmp


def compute_energy(magnitudes, freq_bin):
    """
    compute the total energy use the formula:
        avg E = $ \sum x(n)^2 * I_freq(n) $

    [1 2 3 4 5]    [0 1 0 1 0] = 20

    :param magnitudes:
    :param freq_bin:
    :return:
    """
    magnitudes = np.array(magnitudes)
    freq_bin = np.array(freq_bin)
    return 20*np.log10(np.sum(magnitudes * magnitudes * freq_bin))


def energy_band_feature(frame, f, low_freq, high_freq):
    """
    compute the energy-band frequency feature, which is the centroid frequency of
    specific sub-band.

    :param frame:
    :param f:
    :param low_freq: the minimum frequency in the signal
    :param high_freq: the maximum frequency in the signal
    :return: a time_bin x 6 array
    """
    feat = np.zeros([frame.shape[0], 6])

    mid_freq = (low_freq + high_freq) // 2

    mag_frames = zero_one_normalization(np.abs(frame))

    avg_mag = 0.0
    for line in mag_frames:
        avg_mag = avg_mag + np.sum(line)
    avg_mag = avg_mag / (mag_frames.shape[0] * mag_frames.shape[1])

    for idx in range(frame.shape[0]):

        magnitudes = mag_frames[idx]
        # compute first sub-band feature
        feat[idx][0] = centroid_freq([(element if avg_mag * 0.3 <= element < avg_mag * 0.9 else 0) for element in magnitudes],
                                     [(element if low_freq <= element < mid_freq else 0) for element in f])
        # compute second sub-band feature
        feat[idx][1] = centroid_freq([(e if avg_mag * 0.3 <= e < avg_mag * 0.9 else 0) for e in magnitudes],
                                     [(e if mid_freq <= e <= high_freq else 0) for e in f])
        feat[idx][2] = centroid_freq([(e if avg_mag * 0.9 <= e < avg_mag * 1.8 else 0) for e in magnitudes],
                                     [(e if low_freq <= e <= mid_freq else 0) for e in f])
        feat[idx][3] = centroid_freq([(e if avg_mag * 0.9 <= e < avg_mag * 1.8 else 0) for e in magnitudes],
                                     [(e if mid_freq <= e <= high_freq else 0) for e in f])
        feat[idx][4] = centroid_freq([(e if 1.8 * avg_mag < e else 0) for e in magnitudes],
                                     [(e if low_freq <= e <= mid_freq else 0) for e in f])
        feat[idx][5] = centroid_freq([(e if 1.8 * avg_mag < e else 0) for e in magnitudes],
                                     [(e if mid_freq <= e <= high_freq else 0) for e in f])
        # print('------------------------')

    return feat


def freq_band_feature(frame, f, low_freq, high_freq):
    """
    compute the frequency band energy feature, which is the average energy of the specific
    sub-band

    :param frame:
    :param f:
    :param low_freq:
    :param high_freq:
    :return: a time x 5 array
    """
    feat = np.zeros([frame.shape[0], 5])

    freq_split = np.linspace(low_freq, high_freq, 6, endpoint=True)

    mag_frames = zero_one_normalization(np.abs(frame))

    for idx in range(frame.shape[0]):
        magnitudes = mag_frames[idx]
        # first sub-band feature
        feat[idx][0] = compute_energy(magnitudes, [(1 if freq_split[0] <= e < freq_split[1] else 0) for e in f])
        feat[idx][1] = compute_energy(magnitudes, [(1 if freq_split[1] <= e < freq_split[2] else 0) for e in f])
        feat[idx][2] = compute_energy(magnitudes, [(1 if freq_split[2] <= e < freq_split[3] else 0) for e in f])
        feat[idx][3] = compute_energy(magnitudes, [(1 if freq_split[3] <= e < freq_split[4] else 0) for e in f])
        feat[idx][4] = compute_energy(magnitudes, [(1 if freq_split[4] <= e <= freq_split[5] else 0) for e in f])

    return feat
