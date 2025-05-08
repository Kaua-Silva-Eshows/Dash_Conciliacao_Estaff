import pandas as pd

def initialize_data(id):
    # Dicionário com dados de entrada
    data = {
        "transactionsExtract" : pd.DataFrame(),
        "id": id,
    }

    return data