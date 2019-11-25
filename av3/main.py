import math

import pandas as pd
from sklearn.svm import SVR

columns_to_drop = ["precip_depth_1_hr", "sea_level_pressure", "primary_use", "timestamp"]
target_column = "meter_reading"
train_percentage = 0.8

csv = pd.read_csv("merge_train.csv").drop(columns_to_drop, axis=1).dropna()

y = csv[target_column]
x = csv.drop([target_column], axis=1)

train_size = math.floor(y.size * train_percentage)

y_train = y[:train_size]
x_train = x[:train_size]

y_test = y[train_size+1:]
x_test = x[train_size+1:]

regressor = SVR()
regressor.fit(x_train, y_train)

for i in range(len(y_test)):
    print("Target: {} \t Result: {}".format(y_test.iloc[i], regressor.predict(x_test.iloc[[i]])))
