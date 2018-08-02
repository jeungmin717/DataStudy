

def pandas_index():
    import pandas as pd
    df = pd.read_csv('/templates/data-netflix.csv', engine='python')
    return  df
