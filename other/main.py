import pandas as pd
import json
from collections import defaultdict

data = json.load(open("data/teste.json"))
df = pd.DataFrame()


def decompression_dictionary(colunmns, dictionary, prefix=None):
    """
    Percorre um objeto de json recursivamente e transforma todos os outros objetos e lista de objetos desse json
    em uma lista.
    """

    for key, value in dictionary.items():

        if isinstance(value, dict):
            if prefix is not None:
                decompression_dictionary(colunmns, value, prefix + "_" + key)
            else:
                decompression_dictionary(colunmns, value, key)

        elif isinstance(value, list):
            for v in value:
                if prefix is not None:
                    decompression_dictionary(colunmns, v, prefix + "_" + key)
                else:
                    decompression_dictionary(colunmns, v, key)

        else:
            if prefix is None:
                colunmns.append((key, value))
            else:
                colunmns.append((prefix + "_" + key, value))


def generate_rows(columns):
    grouped_list = defaultdict(list)

    for k, v in columns:
        grouped_list[k].append(v)

    rows = [[] for i in range(1)]

    for key, value in grouped_list.items():

        for i in range(len(value)):

            if i in range(len(rows)):
                rows[i].append(value[i])
            else:
                rows.append([])
                rows[i].append(value[i])

    for i in range(len(rows)):
        if len(rows[i]) < len(max(rows, key=len)):
            n = len(max(rows, key=len)) - (len(rows[i]))
            rows[i] = [None]*n + rows[i]

    return list(grouped_list.keys()), rows


columns_value = []
decompression_dictionary(columns_value, data)

list_columns, list_rows = generate_rows(columns_value)
df = pd.DataFrame(list_rows, columns=list_columns)