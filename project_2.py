import pandas as pd
import quandl

quandl.ApiConfig.api_key = 'gYyp7CLTPWqhbsyFNAN2'
selected = ['CNP', 'F', 'WMT', 'GE', 'TSLA', ]

for symbol in selected:
    data = quandl.get_table('WIKI/PRICES', ticker=symbol,
                            qopts={'columns': ['ticker', 'date', 'adj_close']},
                            date={'gte': '2014-1-1', 'lte': '2016-12-31'},
                            paginate=True
                            )
    stocks = pd.DataFrame(data)
    stocks.to_csv("stock_data_"+symbol+".csv", index=False)

all_files = ['stock_data_CNP.csv', 'stock_data_F.csv',
             'stock_data_WMT.csv', 'stock_data_GE.csv', 'stock_data_TSLA.csv']
df_from_each_file = (pd.read_csv(file) for file in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
print(concatenated_df)
