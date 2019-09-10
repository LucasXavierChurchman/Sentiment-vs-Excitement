import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import prep_data

nba_df = pd.read_csv('data/rNBACombinedScored.csv', sep = ',')
cavs_df = pd.read_csv('data/rCavsScored.csv', sep = ',')
dubs_df = pd.read_csv('data/rDubsScored.csv', sep = ',')
list_dfs = [nba_df, cavs_df, dubs_df]

cols_wanted = ['created_utc', 'sentiment_score', 'score', 'author' ,'author_flair_css_class', 'body']
for df in list_dfs:
    #Filter columns of interest for better readability/usability
    df = df[cols_wanted]
    print (df.head())

# #Adjust each dataframe to capture same time range
# for df in list_o_dfs:
#     df = df[(df['timestamp'] < '2016-06-20 03:00:00') & ]

# df = prep_data.createTimeBins(df, 1000)

# data = df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
# # x = np.linspace(0, data.shape[0], num = data.shape[0])

# # fig, ax = plt.subplots(1, figsize=(16, 3))
# # ax.plot(x, data['sentiment_score']['mean'])
# # plt.show()
