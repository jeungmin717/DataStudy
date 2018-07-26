

def pandas_index():
    import pandas as pd
    df=pd.read_csv('/templates/data-netflix.csv')
    html = df.to_html('a.html')
    return html