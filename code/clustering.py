import random
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def cluster(data, name, log):
    
    pca_2 = PCA(n_components=2)
    low_data = list(pca_2.fit_transform(data))
    # tsne = TSNE(perplexity=200, n_components=2, init='pca', n_iter=250)# TSNE
    # low_data = list(tsne.fit_transform(data))

    if len(low_data) % 2 != 0:
        low_data = low_data[:-1]
        
   
    data_train, data_test = train_test_split(low_data, test_size=0.5)  # , random_state=7)
    estimator = KMeans(n_clusters=4)  
    y_test = estimator.fit_predict(data_test)  
    y_pred = estimator.predict(data_train)

    lable_pred = estimator.labels_  
    centroids = estimator.cluster_centers_  
    inertia = estimator.inertia_  

   
    target_names = ['class 1', 'class 2', 'class 3', 'class 4']
    print('准确度 = ', accuracy_score(y_test, y_pred))
    print('micro-F1 = ', metrics.f1_score(y_test, y_pred, average='micro'))  # precision_score
    print('macro-F1 = ', metrics.f1_score(y_test, y_pred, average='macro'))
    print(classification_report(y_test, y_pred, target_names=target_names))  # 分类报告：precision/recall/fi-score/分类个数
    print('*******************************************************************\n')
    
    if log == 1:
        for i in range(len(low_data)):
            # s:（面积） c :（颜色） marker:（标记） alpha:(透明度)
            if int(lable_pred[i]) == 0:
                plt.scatter(data_train[i][0], data_train[i][1], color='red', s=6.)
            if int(lable_pred[i]) == 1:
                plt.scatter(data_train[i][0], data_train[i][1], color='black', s=6.)
            if int(lable_pred[i]) == 2:
                plt.scatter(data_train[i][0], data_train[i][1], color='blue', s=6.)
            if int(lable_pred[i]) == 3:
                plt.scatter(data_train[i][0], data_train[i][1], color='c', s=6.)

    if log == 2:
        num = 100
        data1 = random.sample(low_data, num)
        data2 = random.sample(low_data, num)
        data3 = random.sample(low_data, num)
        data4 = random.sample(low_data, num)

        for i in range(num):
            # 2.散点图 s （面积）  c （颜色） marker （标记） alpha(透明度)
            plt.scatter(data1[i][0], data1[i][1], color='red', s=10.)
            plt.scatter(data2[i][0], data2[i][1], color='black', s=10.)
            plt.scatter(data3[i][0], data3[i][1], color='blue', s=10.)
            plt.scatter(data4[i][0], data4[i][1], color='c', s=10.)
            # plt.xlim(-2, 2)
            # plt.ylim(-2, 2)

    plt.show()
