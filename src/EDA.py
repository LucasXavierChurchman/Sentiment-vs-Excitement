import numpy as np 
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
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
    df = prep_data.createTimeBins(df, n_bins = 50) 

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


####### Plot mean sentiment scores ######
plt.style.use('seaborn-darkgrid')
matplotlib.rc('lines', linewidth=3)
fig, ((ax1, ax2, ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(20, 8), gridspec_kw={'hspace': 0})

nba_data = nba_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
x = np.linspace(0, nba_data.shape[0], num = nba_data.shape[0])
ax1.plot(x, nba_data['sentiment_score']['mean'], color = 'orangered', alpha = 0.5)
ax1.set_ylim(-2.99,2.99)
ax1.set_title('All Comments (/r/nba)')
plt.grid()

cavs_data = cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_cavs_data = flair_cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
ax2.plot(x, cavs_data['sentiment_score']['mean'], color = 'maroon', alpha = 0.5)
ax2.plot(x, flair_cavs_data['sentiment_score']['mean'], color = 'red', alpha = 0.5)
ax2.set_ylim(-2.99,2.99)
ax2.set_title('Cavaliers Fan Comments')

dubs_data = dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_dubs_data = flair_dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
ax3.plot(x, dubs_data['sentiment_score']['mean'], color = 'darkblue', alpha = 0.5)
ax3.plot(x, flair_dubs_data['sentiment_score']['mean'], color = 'blue', alpha = 0.5)
ax3.set_ylim(-2.99,2.99)
ax3.set_title('Warriors Fan Comments')


for ax in fig.get_axes():
    ax.label_outer()

plt.show()

# ax2.hist(data['sentiment_score']['mean'], color = 'orangered', bins = 50, alpha = 0.5)