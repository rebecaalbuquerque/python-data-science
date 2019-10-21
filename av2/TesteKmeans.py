import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

np.random.seed(42)

data = pd.read_csv('samples\\sample_iris.csv', sep=';')

# Visualize the results on PCA-reduced data
kmeans = KMeans(init='k-means++', n_clusters=2)
kmeans.fit(data)

reduced_data = PCA(n_components=2).fit_transform(data)

for item in reduced_data:
    plt.scatter(item[0], item[1])

plt.show()
