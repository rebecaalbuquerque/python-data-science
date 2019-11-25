import pandas as pd
import av3.redu_mem as rm
from random import randrange


def gen_start_files(root='C:/Users/user/Documents/Ciência dos Dados/Trabalho 3', quantidade='all', remov_year_nan=True,
                    split_dates_feature=True):
    if root[-1] != '/':
        root += '/'
    train_df = pd.read_csv(root + 'train.csv')
    weather_train_df = pd.read_csv(root + 'weather_train.csv')
    test_df = pd.read_csv(root + 'test.csv')
    weather_test_df = pd.read_csv(root + 'weather_test.csv')
    building_meta_df = pd.read_csv(root + 'building_metadata.csv')
    sample_submission = pd.read_csv(root + 'sample_submission.csv')
    train_df["timestamp"] = pd.to_datetime(train_df["timestamp"], format='%Y-%m-%d %H:%M:%S')
    weather_train_df["timestamp"] = pd.to_datetime(weather_train_df["timestamp"], format='%Y-%m-%d %H:%M:%S')
    test_df["timestamp"] = pd.to_datetime(test_df["timestamp"], format='%Y-%m-%d %H:%M:%S')
    weather_test_df["timestamp"] = pd.to_datetime(weather_test_df["timestamp"], format='%Y-%m-%d %H:%M:%S')

    print('Size of train_df data', train_df.shape)
    print('Size of weather_train_df data', weather_train_df.shape)
    print('Size of weather_test_df data', weather_test_df.shape)
    print('Size of building_meta_df data', building_meta_df.shape)

    train_df = rm.reduce_mem_usage(train_df)
    weather_train_df = rm.reduce_mem_usage(weather_train_df)
    building_meta_df = rm.reduce_mem_usage(building_meta_df)
    weather_train_df = weather_train_df.merge(building_meta_df, how='left', left_on='site_id', right_on='site_id')

    if quantidade == 'all':
        chosen_ones = pd.Series(building_meta_df['building_id'].unique()).sample(frac=1)
    else:
        chosen_ones = pd.Series(building_meta_df['building_id'].unique()).sample(n=quantidade)

    weather_train_df = weather_train_df[weather_train_df['building_id'].isin(chosen_ones)]
    train_df = weather_train_df.merge(train_df, how='inner', left_on=['building_id', 'timestamp'],
                                      right_on=['building_id', 'timestamp'])

    test_df = rm.reduce_mem_usage(test_df)
    weather_test_df = rm.reduce_mem_usage(weather_test_df)

    weather_test_df = weather_test_df.merge(building_meta_df, how='left', left_on='site_id', right_on='site_id')
    weather_test_df = weather_test_df[weather_test_df['building_id'].isin(chosen_ones)]

    test_df = weather_test_df.merge(test_df, how='inner', left_on=['building_id', 'timestamp'],
                                    right_on=['building_id', 'timestamp'])

    train_df['floor_count'].fillna(1, inplace=True)
    test_df['floor_count'].fillna(1, inplace=True)

    if remov_year_nan:
        train_df.dropna(subset=['year_built'], inplace=True)
        test_df.dropna(subset=['year_built'], inplace=True)
    else:

        def find_random(x, lista):
            if x == x:
                return x
            else:
                return lista[randrange(len(lista))]

        division = building_meta_df.groupby(['year_built'])['site_id'].count()
        total = sum(division['site_id'])
        division = division['site_id'].apply(lambda a: int((a/total)*100)).to_dict()
        year_list = []
        for key in division.keys():
            year_list += [key] * division[key]

        building_meta_df['year_built'].apply(lambda x: find_random(x, year_list))

    if split_dates_feature:
        train_df['mes'] = train_df['timestamp'].apply(lambda a: a.month)
        train_df['dia'] = train_df['timestamp'].apply(lambda a: a.day)
        train_df['hour'] = train_df['timestamp'].apply(lambda a: a.hour)
        test_df['mes'] = train_df['timestamp'].apply(lambda a: a.month)
        test_df['dia'] = train_df['timestamp'].apply(lambda a: a.day)
        test_df['hour'] = train_df['timestamp'].apply(lambda a: a.hour)

    return [train_df, test_df, sample_submission]
