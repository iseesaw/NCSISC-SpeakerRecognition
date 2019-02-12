# -*- coding: utf-8 -*-
'''
使用sklearn的Gaussian mixture model进行聚类
'''
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.model_selection import StratifiedKFold

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt


def GMM():
    '''

    :return:
    '''
    # 加载数据并切分测试集和训练集
    iris = datasets.load_iris()
    X_train, y_train = iris.data[:-30, :], iris.target[:-30]
    X_test, y_test = iris.data[-30:, :], iris.target[-30:]

    n_classes = 3

    # covariance type: full, diag, tied, spherical
    gmm = GaussianMixture(n_components=n_classes)

    # 使用kmeans初始化
    kmeans = KMeans(n_clusters=n_classes)
    kmeans.fit(X_train)
    centers = kmeans.cluster_centers_
    gmm.means_init = centers

    gmm.fit(X_train)

    # 预测, 计算正确率
    y_train_pred = gmm.predict(X_train)
    y_test_pred = gmm.predict(X_test)
    train_accu = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
    test_accu = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100

    print('train_accuracy={:.2f} test_accuracy={:.2f}'.format(train_accu, test_accu))


if __name__ == '__main__':
    GMM()
