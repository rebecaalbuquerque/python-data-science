import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from av2.NumeroClusterKMEANS import calculate_wcss, optimal_number_of_clusters

"""
    Colunas da base 'sample_pinheiro_75MB' => id, avg, std, item_count, sec_count, max_unitario, min, total, max
"""
cols = ['avg', 'std', 'item_count', 'sec_count', 'max_unitario', 'min', 'total', 'max']

comeco = datetime.datetime.now()
print(comeco)

# data = pd.read_csv('samples\\sample_pinheiro_75MB.csv', sep=';', usecols=cols).head(2000)
data = pd.read_csv('C:\\Users\\user\\Downloads\\dadosTransacoes\\cupons_15.csv', sep=';', usecols=cols)

for coluna in data.columns:
    data[coluna] = data[coluna]/(max(data[coluna]))

# Descobrindo quantidade de clusters
sum_of_squares = calculate_wcss(data)
n = optimal_number_of_clusters(sum_of_squares)

# Algoritmo de cluster
kmeans = KMeans(n_clusters=n)
data['cluster'] = kmeans.fit_predict(data)

# Algoritmo de redução de dimensionalidade
reduced_data = TSNE(n_components=2).fit_transform(data)

# Montando DataFrame do resultado
results = pd.DataFrame(reduced_data, columns=['x', 'y'])

data['tsne_x'] = reduced_data.T[0, :]
data['tsne_y'] = reduced_data.T[1, :]

# results.to_csv("resultados\\saida.csv")
data.to_csv('resultados\\saida.csv', sep=';')

# Plotando resultado final
sns.scatterplot(x="x", y="y", hue=data['cluster'], data=results)
plt.title("K-means Clustering - TSNE")
plt.show()

fim = datetime.datetime.now()
print(fim)
print(fim-comeco)
print("n clusters =", n)
print(cols)
