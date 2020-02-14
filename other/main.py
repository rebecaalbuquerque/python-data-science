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

# todo: não gerar o DF e sim as rows do DF
def generate_rows(columns):
    grouped_list = defaultdict(list)

    for k, v in columns:
        grouped_list[k].append(v)

    df = pd.DataFrame(columns=list(grouped_list.keys()))
    row = [[]]

    for index, key in enumerate(grouped_list.items()):
        index

columns_value = []
decompression_dictionary(columns_value, data)

generate_rows(columns_value)