import csv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

if __name__ == '__main__':

    lista_inteiros = []
    X = np.empty(0, dtype=float)
    Y = np.empty(0, dtype=float)

    with open('C:\\Users\\user\\Downloads\\dadosTransacoes\\cupons_7.csv', 'r')as f:
        data = csv.reader(f, delimiter=';')

        for i, row in enumerate(data):

            if i == 0:
                continue
            else:
                arr = [float(row[0]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])]
                lista_inteiros.append(arr)

            if i == 500:
                break

    X = np.array(lista_inteiros)
    Y = np.append(X, list(range(len(Y))))

    tsne = TSNE(n_components=2, random_state=0)
    reduced_data = tsne.fit_transform(X)

    plt.figure(figsize=(6, 5))

    for i in reduced_data:
        plt.scatter(i[0], i[1])

    plt.legend()
    plt.show()
