import pandas as pd

df1 = pd.read_csv('data/Game7-1stHalf.csv', sep = ',')
df2 = pd.read_csv('data/Game7-2ndHalf.csv', sep = ',')
print(df1.size, df2.size, df1.size + df2.size)