import PrepData
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
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

nba_data = nba_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
cavs_data = cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_cavs_data = flair_cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
dubs_data = dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_dubs_data = flair_dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])

# np.corr(nba_data['sentiment_score']['mean'],cavs_data['sentiment_score']['mean'])

d = {'nba_sentiment': nba_data['sentiment_score']['mean'].values,
     'cavs_sentiment': cavs_data['sentiment_score']['mean'].values,
     'flair_cavs_sentiment': flair_cavs_data['sentiment_score']['mean'].values,
     'dubs_sentiment': dubs_data['sentiment_score']['mean'].values,
     'flair_dubs_sentiment': flair_dubs_data['sentiment_score']['mean'].values,
     'nba_density': nba_data['sentiment_score']['size'].values,
     'cavs_density': cavs_data['sentiment_score']['size'].values,
     'flair_cavs_density': flair_cavs_data['sentiment_score']['size'].values,
     'dubs_density': dubs_data['sentiment_score']['size'].values,
     'flair_dubs_density': flair_dubs_data['sentiment_score']['size'].values
     }

df = pd.DataFrame(data = d)


plt.figure(figsize=(5,5))
plt.title('Sentiment and Density Correlation Heatmap')
sns.heatmap(df.corr(),
            vmin=-1,
            cmap='magma', #https://www.youtube.com/watch?v=yVo1S52xdpI
            annot=True)

plt.show()