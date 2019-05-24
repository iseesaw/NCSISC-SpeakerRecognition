import numpy as np
import h5py
from utils.wrappers import check_path_existence
import soundfile as sf
from utils import signalproc
from utils import doppler_feature
import textgrid


class PhomeFrame(object):

    """

    """
    def __init__(self, input_file_name=''):
        self.feats = np.empty(0, dtype='|O')
        self.starts = np.empty(0, dtype='|O')
        self.ends = np.empty(0, dtype='|O')

        if input_file_name == '':
            pass
        else:
            pf = PhomeFrame.read(input_file_name)

            self.feats = pf.feats
            self.starts = pf.feats
            self.ends = pf.ends

    @staticmethod
    def read(input_file_name):
        pf = PhomeFrame()

        with h5py.File(input_file_name, 'r') as f:
            pf.feats = f.get('feats').value
            pf.starts = f.get('starts').value
            pf.ends = f.get('ends').value

        pf.starts = pf.starts.astype(np.int)
        pf.ends = pf.ends.astype(np.int)
        return pf

    @check_path_existence
    def write(self, output_file_name):
        f = h5py.File(output_file_name, 'w')

        f.create_dataset('feats', self.feats.shape, 'd', self.feats)
        f.create_dataset('starts', self.starts.shape, 'd', self.starts)
        f.create_dataset('ends', self.ends.shape, 'd', self.ends)
        f.close()

    @staticmethod
    def read_raw(wav_file_name, textgrid_file_name):
        pf = PhomeFrame()

        x, fs = sf.read(wav_file_name)
        x = signalproc.wavelet_denoising(x)
        x = signalproc.preemphasis(x)
        x = signalproc.bin_butterworth_filtering(x, fs, 19800, 20200)

        tg = textgrid.TextGrid.fromFile(textgrid_file_name)
        t_starts = []
        t_ends = []
        for i, seg in enumerate(tg[0]):
            start, end, mark = seg.minTime, seg.maxTime, seg.mark

            if mark != "":
                t_starts.append(start)
                t_ends.append(end)

        f, t, frame = signalproc.framesig(x, fs, 0.025*fs, 0.01*fs)

        feats = None

        starts = []
        ends = []
        for i in range(len(t_starts)):
            t_start = t_starts[i]
            t_end = t_ends[i]

            start = np.argmin(np.abs(float(t_start) - t))
            end = np.argmin(np.abs(float(t_end) - t)) + 1

            freq_feats = doppler_feature.freq_band_feature(frame[start:end], f, 19800, 20200)
            freq_feats = doppler_feature.zscore_normalization(freq_feats)
            energy_feats = doppler_feature.energy_band_feature(frame[start:end], f, 19800, 20200)
            # energy_feats = doppler_feature.zscore_normalization(energy_feats)
            feat = np.concatenate((freq_feats, energy_feats), axis=1)
            if feats is None:
                starts.append(0)
                ends.append(feat.shape[0])
                feats = feat
            else:
                starts.append(feats.shape[0])
                ends.append(feats.shape[0] + feat.shape[0])
                feats = np.concatenate((feats, feat), axis=0)

        pf.feats = np.array(feats)
        pf.starts = np.array(starts)
        pf.ends = np.array(ends)
        return pf

    def number_of_phones(self):
        return self.starts.shape[0]

    def number_of_frames(self):
        return self.feats.shape[0]

    def get_all_phome_feature_as_one(self):
        one_feats = []
        for i in range(self.starts.shape[0]):
            start = self.starts[i]
            end = self.ends[i]
            one_feats.append(self.feats[start:end])

        return np.array(one_feats)


