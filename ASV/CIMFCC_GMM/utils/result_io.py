from sklearn.mixture import GaussianMixture as GMM
import numpy as np
import sys
import h5py
import os
from sidekit.sidekit_wrappers import *


workdirPath = os.path.dirname(os.path.abspath(__file__))

def gmm_read(gmm, input_file_name, prefix=''):
    assert isinstance(gmm, GMM), 'First parameter should be a GMM'

    with h5py.File(os.path.join(workdirPath, input_file_name), 'r') as f:
        gmm.weights_ = f.get(prefix+'weights_').value
        gmm.means_ = f.get(prefix+'means_').value
        gmm.covariances_ = f.get(prefix+'covariances_').value
        gmm.precisions_ = f.get(prefix+'precisions_').value
        gmm.precisions_cholesky_ = f.get(prefix+'precisions_cholesky_').value


@check_path_existance
def gmm_write(gmm, output_file_name, prefix='', mode='w'):
    assert isinstance(gmm, GMM), 'First parameter should be a GMM'

    f = h5py.File(os.path.join(workdirPath, output_file_name), mode)

    f.create_dataset(prefix+'weights_', gmm.weights_.shape, 'd', gmm.weights_, 
        compression='gzip', fletcher32=True)
    f.create_dataset(prefix+'means_', gmm.means_.shape, 'd', gmm.means_, 
        compression='gzip', fletcher32=True)
    f.create_dataset(prefix+'covariances_', gmm.covariances_.shape, 'd', gmm.covariances_,
        compression='gzip', fletcher32=True)
    f.create_dataset(prefix+'precisions_', gmm.precisions_.shape, 'd', gmm.precisions_, 
        compression='gzip', fletcher32=True)
    f.create_dataset(prefix+'precisions_cholesky_', gmm.precisions_cholesky_.shape, 'd', gmm.precisions_cholesky_,
        compression='gzip', fletcher32=True)
    f.close()


@check_path_existance
def feat_write(feat, output_file_name, prefix='', mode='w'):
    assert isintance(feat, np.mat), 'First parameter should be a numpy matrix'

    f = h5py.File(os.path.join(workdirPath, output_file_name), mode)

    f.create_dataset(prefix+'features', feat.shape, 'd', feat, compression='gzip', fletcher32=True)
    f.close()


@check_path_existance
def feat_read(feat, input_file_name, prefix=''):
    with h5py.File(os.path.join(workdirPath, output_file_name), 'r') as f:
        feat = f.get(prefix+'features').value

        


