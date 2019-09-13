import numpy as np 
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import PrepData
import scipy.stats as stats
plt.style.use('seaborn-darkgrid')
bins = 50

default_df = pd.read_csv('data/rNBACombinedScored.csv', sep = ',', low_memory = False)
custom_df = pd.read_csv('data/rNBACombinedScoredCustom.csv', sep = ',', low_memory = False)

# #People were particularly angry here so its a good place to verify the custom lexicon is working
# print(default_df[['body', 'sentiment_score']].loc[5795:5805])
# print(custom_df[['body', 'sentiment_score']].loc[5795:5805])

default_df, custom_df = PrepData.bin_dfs([default_df, custom_df], bins)

default_data = default_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
custom_data = custom_df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])

def plot_sentiment():
    matplotlib.rc('lines', linewidth=3)
    fig, ax = plt.subplots(figsize=(15, 4))

    x = np.linspace(0, default_data.shape[0], num = default_data.shape[0])
    ax.plot(x, default_data['sentiment_score']['mean'], color = 'blue', alpha = 0.5)
    ax.plot(x, custom_data ['sentiment_score']['mean'], color = 'red', alpha = 0.5)

    ax.set_ylim(-3,3)
    ax.hlines(0, 0, bins, linestyles = 'dashed')
    ax.set_title('r/NBA Sentiment')
    ax.legend(('default lexicon','custom lexicon'), loc = 'upper left')

    plt.subplots_adjust(top=0.975,
                        bottom=0.025,
                        left=0.025,
                        right=0.975,
                        hspace=0.07,
                        wspace=0.05)

    plt.show()

def hyp_test():
    print('Test null hypothesis that mean sentiment scores using customized dictionary are the same\n')
    alpha = 0.05
    def_mean = np.mean(default_data['sentiment_score']['mean'])
    def_sd = np.std(default_data['sentiment_score']['mean'])
    def_n= default_data['sentiment_score']['mean'].size

    cus_mean = np.mean(custom_data['sentiment_score']['mean'])
    cus_sd = np.std(custom_data['sentiment_score']['mean'])
    cus_n = custom_data['sentiment_score']['mean'].size

    print(def_n)
    
    se = np.sqrt((def_sd**2/def_n)+(cus_sd**2/cus_n))

    t = ((def_mean - cus_mean)/se)
    pval = stats.norm.pdf(t)
    print('Mean using default dictionary: \t', def_mean)
    print('Mean using custom dictionary: \t', cus_mean)
    print('test statistic: \t\t', t)
    # print('p-value: \t\t\t', '%f' % (pval))
    print('p-value: \t\t\t', pval)

    if pval < alpha:
        print('\nReject null hypothesis')
    else:
        print('\nFail to reject null hypothesis')

    # print(stats.ttest_ind(default_data['sentiment_score']['mean'], custom_data['sentiment_score']['mean']))

if __name__ == "__main__":
    hyp_test()
    plot_sentiment()
    
