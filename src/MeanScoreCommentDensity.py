####### Plot mean sentiment scores and comment densities ######
import numpy as np 
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import PrepData
plt.style.use('seaborn-darkgrid')
bins = 50

nba_df = pd.read_csv('data/rNBACombinedScored.csv', sep = ',', low_memory = False)
cavs_df = pd.read_csv('data/rCavsScored.csv', sep = ',')
dubs_df = pd.read_csv('data/rDubsScored.csv', sep = ',')

#Create data frames for comments from the /r/nba thread by fans of either team based on their flair
flair_cavs_df = nba_df[nba_df['author_flair_css_class'].str.contains('Cavaliers', na = False)]
flair_dubs_df = nba_df[nba_df['author_flair_css_class'].str.contains('Warriors', na = False)]

list_dfs = [nba_df, flair_cavs_df, flair_dubs_df, cavs_df, dubs_df]

nba_df, flair_cavs_df, flair_dubs_df, cavs_df, dubs_df = PrepData.bin_dfs(list_dfs, bins)


matplotlib.rc('lines', linewidth=3)
fig, ((ax1, ax2, ax3),(ax4, ax5, ax6)) = plt.subplots(2,3,figsize=(15, 4))

#rNba
nba_data = nba_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
nba_data.to_csv('data/rNBAbinned.csv')
x = np.linspace(0, nba_data.shape[0], num = nba_data.shape[0])
ax1.plot(x, nba_data['sentiment_score']['mean'], color = 'orangered', alpha = 0.5)
ax1.set_ylim(-3,3)
ax1.hlines(0, 0, bins, linestyles = 'dashed')
ax1.set_title('r/NBA Sentiment v Time')
ax1.legend(('r/NBA',), loc = 'upper left')

ax4.plot(x, nba_data['sentiment_score']['size'], color = 'orangered', alpha = 0.5)
ax4.set_title('r/NBA Comment Density (comments / 3.3 minute period)')
ax4.legend(('r/NBA',), loc = 'upper left')
plt.grid()

#Cavs
cavs_data = cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_cavs_data = flair_cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
ax2.plot(x, cavs_data['sentiment_score']['mean'], color = 'maroon', alpha = 0.5)
ax2.plot(x, flair_cavs_data['sentiment_score']['mean'], color = 'red', alpha = 0.5)
ax2.set_ylim(-3,3)
ax2.hlines(0, 0, bins, linestyles = 'dashed')
ax2.set_title('Cavaliers Sentiment v Time')
ax2.legend(('r/ClevelandCavs','r/NBA Cavs Flair'), loc = 'upper left')

ax5.plot(x, cavs_data['sentiment_score']['size'], color = 'maroon', alpha = 0.5)
ax5.plot(x, flair_cavs_data['sentiment_score']['size'], color = 'red', alpha = 0.5)
ax5.set_title('Cavaliers Comment Density (comments / 3.3 minute period)')
ax5.legend(('r/ClevelandCavs','r/NBA Cavs Flair'), loc = 'upper left')

#Warriors
dubs_data = dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_dubs_data = flair_dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
ax3.plot(x, dubs_data['sentiment_score']['mean'], color = 'darkblue', alpha = 0.5)
ax3.plot(x, flair_dubs_data['sentiment_score']['mean'], color = 'turquoise', alpha = 0.5)
ax3.set_ylim(-3,3)
ax3.hlines(0, 0, bins, linestyles = 'dashed')
ax3.set_title('Warriors Sentiment v Time')
ax3.legend(('r/Warriors','r/NBA Warriors Flair'), loc = 'upper left')

ax6.plot(x, dubs_data['sentiment_score']['size'], color = 'darkblue', alpha = 0.5)
ax6.plot(x, flair_dubs_data['sentiment_score']['size'], color = 'turquoise', alpha = 0.5)
ax6.set_title('Warriors Comment Density (comments / 3.3 minute period)')
ax6.legend(('r/Warriors','r/NBA Warriors Flair'), loc = 'upper left')

plt.grid()

plt.subplots_adjust(top=0.975,
                    bottom=0.025,
                    left=0.025,
                    right=0.975,
                    hspace=0.07,
                    wspace=0.05)


ax1.label_outer()
ax2.label_outer()
ax3.label_outer()

plt.show()