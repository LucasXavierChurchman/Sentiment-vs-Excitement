import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import prep_data

nba_df = pd.read_csv('data/rNBACombinedScored.csv', sep = ',')
cavs_df = pd.read_csv('data/rCavsScored.csv', sep = ',')
dubs_df = pd.read_csv('data/rDubsScored.csv', sep = ',')
list_dfs = [nba_df, cavs_df, dubs_df]

cols_wanted = ['created_utc','sentiment_score','score','author','author_flair_css_class','body']
for i, df in enumerate(list_dfs):
    #Filter columns of interest for better readability/usability
    df = df[cols_wanted]

    #make a more human-readable timestamp column (datetime format instead of unix)
    df = prep_data.convertUTC(df, 'created_utc', 'created_utc_dt')

    #Filter dfs to have data from same time ranges
    df = df[(df['created_utc_dt'] >= '2016-06-20 00:00:00') & (df['created_utc_dt'] <= '2016-06-20 02:45:00')]

    #create time bins
    df = prep_data.createTimeBins(df, 1000)

    #printing first and last rows to make sure things look ok
    print(i,'-------------------------------------\n', df[::df.shape[0]-1] )
    list_dfs[i] = df
    
nba_df, cavs_df, dubs_df = list_dfs[0], list_dfs[1], list_dfs[2]

# df = prep_data.createTimeBins(df, 1000)

# data = df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
# # x = np.linspace(0, data.shape[0], num = data.shape[0])

# # fig, ax = plt.subplots(1, figsize=(16, 3))
# # ax.plot(x, data['sentiment_score']['mean'])
# # plt.show()
