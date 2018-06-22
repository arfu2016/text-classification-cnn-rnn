"""
@Project   : text-classification-cnn-rnn
@Module    : kmeans_k.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/22/18 3:38 PM
@Desc      : 
"""
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()


def sklearn_kMeans(i):
    model = KMeans(n_clusters=i, random_state=0)
    # print('data shape:', iris.data.shape)
    model.fit(iris.data)
    # print('labels:', model.labels_)
    # print('distances:', model.transform(iris.data))
    distances = model.transform(iris.data)
    in_distance = []
    for j in range(i):
        in_distance.append(np.mean(distances[model.labels_ == j, j]))
    out_distance = avg_distance(model.cluster_centers_)
    return in_distance, out_distance


def avg_distance(np_array):
    num, _ = np_array.shape
    sum_distance = 0
    k = 0
    for i in range(num-1):
        for j in range(i+1, num):
            res = sum((np_array[i, :] - np_array[j, :])**2)
            res = res**0.5
            sum_distance += res
            k += 1
    return sum_distance/k


if __name__ == '__main__':
    w1, w2 = 1, 1
    for i in range(2, 10):
        inside_dis, outside_dis = sklearn_kMeans(i)
        result = w2*outside_dis/(w1*np.mean(inside_dis))
        result2 = w2*outside_dis - w1*np.mean(inside_dis)
        print(result, result2, np.mean(inside_dis), outside_dis)
        # 如果kmeans中的k增加1，能使得类内平均距离大幅减小，而类间平均距离减小有限的话，
        # 应该把k增加1，能得到更好的聚类效果
