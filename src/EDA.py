import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import prep_data

nba_df = pd.read_csv('data/rNBACombinedScored.csv', sep = ',')
cavs_df = pd.read_csv('data/rCavsScored.csv', sep = ',')
dubs_df = pd.read_csv('data/rDubsScored.csv', sep = ',')

#Create data frames for comments from the /r/nba thread by fans of either team based on their flair
flair_cavs_df = nba_df[nba_df['author_flair_css_class'].str.contains('Cavaliers', na = False)]
flair_dubs_df = nba_df[nba_df['author_flair_css_class'].str.contains('Warriors', na = False)]

list_dfs = [nba_df, flair_cavs_df, flair_dubs_df, cavs_df, dubs_df]

cols_wanted = ['created_utc','sentiment_score','score','author','author_flair_css_class','body']
for i, df in enumerate(list_dfs):
    #Filter columns of interest for better readability/usability
    df = df[cols_wanted]

    #make a more human-readable timestamp column (datetime format instead of epoch)
    df = prep_data.convertUTC(df, 'created_utc', 'created_utc_dt')

    #Filter dfs to have data from same time ranges
    df = df[(df['created_utc_dt'] >= '2016-06-20 00:00:00') & (df['created_utc_dt'] <= '2016-06-20 02:45:00')]

    #create time bins. 330 bins will make slices of roughly 30 seconds
    df = prep_data.createTimeBins(df, n_bins = 100) 

    #printing first and last rows to make sure things look ok
    # print(i,'-------------------------------------\n', df[::df.shape[0]-1] )

    list_dfs[i] = df

#reassin names to the dataframes
nba_df, flair_cavs_df, flair_dubs_df, cavs_df, dubs_df = [list_dfs[x] for x in range(len(list_dfs))]


names = ['r/NBA Comments',
        'r/NBA Comments with Cavaliers Flair',
        'r/NBA Comments with Warriors Flair',
        'r/ClevelandCavs comments'
        'r/Warriors comments']


#Plot mean sentiment scores
fig, axs = plt.subplots(3,2,figsize=(16, 30))
data = nba_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
x = np.linspace(0, data.shape[0], num = data.shape[0])
axs[0,0].plot(x, data['sentiment_score']['mean'], color = 'black', alpha = 0.5)
axs[0,0].set_ylim(-3,3)
plt.grid()
axs[0,1].hist(data['sentiment_score']['mean'], color = 'black', bins = 100, alpha = 0.5)
# axs[0].set_title('All /r/NBA comments')
plt.grid()

plt.show()