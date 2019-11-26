import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR

path = str(Path().absolute().parent.parent) + "\\energydados2\\"
columns_to_drop = ["precip_depth_1_hr", "sea_level_pressure", "primary_use", "timestamp", "meter"]
target_column = "meter_reading"
train_percentage = 0.8

csv = pd.read_csv(path + "merge_train.csv").drop(columns_to_drop, axis=1).dropna()

for coluna in csv.columns:
    csv[coluna] = csv[coluna] / (max(csv[coluna]))

y = csv[target_column]
x = csv.drop([target_column], axis=1)

train_size = math.floor(y.size * train_percentage)

y_train = y[:train_size]
x_train = x[:train_size]

y_test = y[train_size + 1:]
x_test = x[train_size + 1:]

regressor = SVR()
regressor.fit(x_train, y_train)

y_predict = regressor.predict(x_test)

for target, result in zip(y_test, y_predict):
    print("Target: {} \t Predicted: {}".format(target, result))

x_ax = range(y_test.size)

plt.scatter(x_ax, y_test, s=5, color="blue", label="target")
plt.plot(x_ax, y_predict, color="red", label="predicted")
plt.legend()
plt.show()

score = regressor.score(x_test, y_test)
print(score)

mse = mean_squared_error(y_test, y_predict)
print("Mean Squared Error:", mse)

rmse = math.sqrt(mse)
print("Root Mean Squared Error:", rmse)
