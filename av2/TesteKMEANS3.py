import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from av2.NumeroClusterKMEANS import calculate_wcss, optimal_number_of_clusters

# preparando dados
iris = sns.load_dataset('iris')
df = iris.drop('species', axis=1)

# calculando a soma dos quadrados para as 19 quantidade de clusters
sum_of_squares = calculate_wcss(df)

# calculando a quantidade ótima de clusters
n = optimal_number_of_clusters(sum_of_squares)

# inicializando o kmeans para nossa quantidade ótima de clusters
kmeans = KMeans(n_clusters=n)

# predizendo nossos clusters
iris['clusters'] = kmeans.fit_predict(df)

# transformando as especies de iris em numeros para colorir o gráfico
iris['species_encoded'] = LabelEncoder().fit_transform(iris['species'])

plt.figure(figsize=(15,5))

plt.subplot(1, 2, 1)
plt.title('Antes')
plt.xlabel('comprimento da pétala')
plt.ylabel('largura da pétala')
plt.scatter(iris['petal_length'], iris['petal_width'], c=iris['species_encoded'])


plt.subplot(1, 2, 2)
plt.title('Depois')
plt.xlabel('comprimento da pétala')
plt.scatter(iris['petal_length'], iris['petal_width'], c=iris['clusters'])

plt.show()