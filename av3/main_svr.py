import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from av3.util.file_util import get_train_and_test
from av3.util.paths import path_output_data

path = str(Path().absolute().parent.parent) + "\\energydados2\\"
columns_to_drop = ["precip_depth_1_hr", "sea_level_pressure", "primary_use", "timestamp", "meter", "site_id"]
target_column = "meter_reading"
train_percentage = 0.8

df = pd.read_csv(path_output_data + "merge_train.csv").drop(columns_to_drop, axis=1).dropna()

# Normalizando os dados do CSV
for coluna in df.columns:
    df[coluna] = df[coluna] / (max(df[coluna]))

# Gerando os dados de treino e teste
x_train, y_train, x_test, y_test = get_train_and_test(df, target_column, train_percentage)

# Configurando o algoritmo para fazer a regressão e gerando o resultado a partir dos dados de teste
regressor = SVR()
regressor.fit(x_train, y_train)

y_predict = regressor.predict(x_test)

#
for target, result in zip(y_test, y_predict):
    print("Target: {} \t Predicted: {}".format(target, result))

# Gerando estatísticas do resultado da regressão
score = regressor.score(x_test, y_test)
print("Score:", score)

mse = mean_squared_error(y_test, y_predict)
print("Mean Squared Error:", mse)

rmse = math.sqrt(mse)
print("Root Mean Squared Error:", rmse)

# Plotando gráfico
x_ax = range(y_test.size)

plt.scatter(x_ax, y_test, s=5, color="blue", label="target")
plt.plot(x_ax, y_predict, color="red", label="predicted")
plt.legend()
plt.show()
