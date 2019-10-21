import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from av2.NumeroClusterKMEANS import calculate_wcss, optimal_number_of_clusters

"""
    Colunas da base 'sample_pinheiro_75MB' => id, avg, std, item_count, sec_count, max_unitario, min, total, max
"""
cols = ['avg', 'std', 'item_count', 'sec_count', 'min', 'total', 'max']
is_tsne = True

comeco = datetime.datetime.now()
print(comeco)

data = pd.read_csv('samples\\sample_pinheiro_75MB.csv', sep=';', usecols=cols)

# Descobrindo quantidade de clusters
sum_of_squares = calculate_wcss(data)
n = optimal_number_of_clusters(sum_of_squares)

# Algoritmo de cluster
kmeans = KMeans(n_clusters=n)
data['clusters'] = kmeans.fit_predict(data)

# Algoritmo de redução de dimensionalidade
if not is_tsne:
    reduced_data = PCA(n_components=2).fit_transform(data)
else:
    reduced_data = TSNE(n_components=2).fit_transform(data)

# Montando DataFrame do resultado
results = pd.DataFrame(reduced_data, columns=['x', 'y'])

# Plotando resultado final
sns.scatterplot(x="x", y="y", hue=data['clusters'], data=results)
plt.title("K-means Clustering - TSNE" if is_tsne else "K-means Clustering - PCA")
plt.show()

fim = datetime.datetime.now()
print(fim)
print(fim-comeco)
print("n clusters =", n)
print(cols)
