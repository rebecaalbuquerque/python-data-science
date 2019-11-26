import math


def get_train_and_test(df, target_column, train_percentage):
    y = df[target_column]
    x = df.drop([target_column], axis=1)

    train_size = math.floor(y.size * train_percentage)

    y_train = y[:train_size]
    x_train = x[:train_size]

    y_test = y[train_size + 1:]
    x_test = x[train_size + 1:]

    return x_train, y_train, x_test, y_test
