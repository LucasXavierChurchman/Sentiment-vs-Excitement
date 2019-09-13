####### Plot mean sentiment scores and comment densities overlapping######
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

nba_data = nba_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
cavs_data = cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_cavs_data = flair_cavs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
dubs_data = dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
flair_dubs_data = flair_dubs_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])

def plot_sentiment():
    matplotlib.rc('lines', linewidth=3)
    fig, ax = plt.subplots(figsize=(15, 4))

    x = np.linspace(0, nba_data.shape[0], num = nba_data.shape[0])
    ax.plot(x, nba_data['sentiment_score']['mean'], color = 'orangered', alpha = 0.5)
    ax.plot(x, cavs_data['sentiment_score']['mean'], color = 'maroon', alpha = 0.5)
    ax.plot(x, flair_cavs_data['sentiment_score']['mean'], color = 'red', alpha = 0.5)
    ax.plot(x, dubs_data['sentiment_score']['mean'], color = 'darkblue', alpha = 0.5)
    ax.plot(x, flair_dubs_data['sentiment_score']['mean'], color = 'turquoise', alpha = 0.5)

    ax.set_ylim(-4,4)
    ax.hlines(0, 0, bins, linestyles = 'dashed')
    ax.set_title('Sentiment v Time')
    ax.set_xlabel('Time Slice (1 slice = 3.3 minutes)')
    ax.legend(('r/NBA','r/ClevelandCavs','r/NBA Cavs Flair','r/Warriors','r/NBA Warriors Flair'), loc = 'upper left')

    plt.subplots_adjust(top=0.975,
                        bottom=0.025,
                        left=0.025,
                        right=0.975,
                        hspace=0.07,
                        wspace=0.05)
    plt.show()

def plot_density():
    matplotlib.rc('lines', linewidth=3)
    fig, ax = plt.subplots(figsize=(20, 4))

    x = np.linspace(0, nba_data.shape[0], num = nba_data.shape[0])
    # ax.plot(x, nba_data['sentiment_score']['size'], color = 'orangered', alpha = 0.5) # skews the plot
    ax.plot(x, cavs_data['sentiment_score']['size'], color = 'maroon', alpha = 0.5)
    ax.plot(x, flair_cavs_data['sentiment_score']['size'], color = 'red', alpha = 0.5)
    ax.plot(x, dubs_data['sentiment_score']['size'], color = 'darkblue', alpha = 0.5)
    ax.plot(x, flair_dubs_data['sentiment_score']['size'], color = 'turquoise', alpha = 0.5)

    ax.set_title('Comment Density v Time')
    ax.set_xlabel('Time Slice (1 slice = 3.3 minutes)')
    ax.legend(('r/ClevelandCavs','r/NBA Cavs Flair','r/Warriors','r/NBA Warriors Flair'), loc = 'upper left')

    plt.subplots_adjust(top=0.94,
                        bottom=0.055,
                        left=0.025,
                        right=0.995,
                        hspace=0.07,
                        wspace=0.05)
    plt.show()

if __name__ == "__main__":
    # plot_sentiment()
    plot_density()