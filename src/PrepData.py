'''
Class with functions to help organize, combine, generate data
'''

import numpy as np 
import pandas as pd 
from afinn import Afinn
from afinn_custom import Afinn as Afinn_Custom

af = Afinn(emoticons=True)
af_c = Afinn_Custom(emoticons=True)

def combine_dfs(list_of_dfs):
    '''Used in the case multiple datasets need to be combined
    Parameters: 
    -----------
    list_of_dfs: list object of dataframes

    Returns
    -------
    Pandas DataFrame
    '''
    df = list_of_dfs[0]
    for data_frame in list_of_dfs[1:]:
        df = df.append(data_frame).sort_values(['created_utc'], ascending = True)
    return df

def convert_utc(df, epoch_time_col_name, new_col_name):
    '''Uses a timestamp column w/ epochformat to create a new one with 'normal' UTC timestamp format
      Parameters: 
    -----------
    df: Pands dataframe with epoch timestamp
    epoch_time_col_name: str, name of epoch time column
    new_col_name: str, name for the new column

    Returns
    -------
    Pandas DataFrame
    '''
    df.insert(0, new_col_name, pd.to_datetime(df[epoch_time_col_name], unit='s'))
    # df['dt_created_utc'] = pd.to_datetime(df[epoch_time_col_name], unit='s')
    return df

def calc_sentiment_scores(df, comment_text_col_name):
    '''Calculates a list of sentiment scores for each text string in the df specified by text_col_name
    and adds it to the dataframe

    Parameters:
    ----------
    df: pandas dataframe with comment column
    text_col_name: string, name of the column with text strings to be scored

    Returns
    -------
    Pandas DataFrame
    '''
    sentiment_scores = []
    for comment in df[comment_text_col_name]:
        try:
            sentiment_scores.append(af.score(comment))
        except:
            sentiment_scores.append(np.nan)

    df['sentiment_score'] = sentiment_scores
    return df

def calc_sentiment_scores_custom(df, comment_text_col_name):
    '''
    Same as function above but uses custom Afinn library with different lexicon
    Parameters:
    ----------heatmap
    df: pandas dataframe with comment cheatmapolumn
    text_col_name: string, name of the heatmapcolumn with text strings to be scored
heatmap
    Returns
    -------
    Pandas DataFrame
    '''
    sentiment_scores = []
    for comment in df[comment_text_col_name]:
        try:
            sentiment_scores.append(af_c.score(comment))
        except:
            sentiment_scores.append(np.nan)

    df['sentiment_score'] = sentiment_scores
    return df

def create_time_bins(df, n_bins = 50):
    '''
    Creates bins of time periods we can use to compute statistics based on them

    Parameters: 
    -----------
    df: Pandas data frame. Assumes 'created_utc' column exists using epoch time format
    n_bins: number of time periods we want to cut the data into. Higher will give more granular results

    Returns:
    ----------
    Pandas DataFrame
    '''
    df.insert(1, 'time_slice', pd.cut(df['created_utc'], bins = n_bins))#, labels = range(n_bins)))
    return df

def bin_dfs(listDFs, n_bins = 50):
    '''
    Creates times bins for each dataframe in listDFS
    note: this is function is only really useful in this particular case/structure of data. Also
    reduces columns which should be another function. It works for this particular project so 
    we'll roll with it.

    Parameters
    -----------
    listDFs: list of dataframes

    Returns
    ----------
    list of dataframes
    '''
    colsWanted = ['created_utc','sentiment_score','score','author','author_flair_css_class','body']
    binnedDFs = []
    for df in listDFs:
        df = df[colsWanted]
        df = convert_utc(df, 'created_utc', 'created_utc_dt')
        df = df[(df['created_utc_dt'] >= '2016-06-20 00:00:00') & (df['created_utc_dt'] <= '2016-06-20 02:45:00')]
        df = create_time_bins(df, n_bins) 
        binnedDFs.append(df)

    return [binnedDFs[x] for x in range(len(binnedDFs))]
    
if __name__ == "__main__":
    df1 = pd.read_csv('data/rNBA1stHalf.csv', sep = ',')
    df2 = pd.read_csv('data/rNBA2ndHalf.csv', sep = ',')
    rNBA_dfs = [df1, df2]
    rNBA_df = combine_dfs(rNBA_dfs)
    rNBA_df = calc_sentiment_scores(rNBA_df, 'body')
    rNBA_df.to_csv('data/rNBACombinedScored.csv')
    #generate with customized lexicon
    rNBA_df = combine_dfs(rNBA_dfs)
    rNBA_df_custom = calc_sentiment_scores_custom(rNBA_df, 'body')
    rNBA_df_custom.to_csv('data/rNBACombinedScoredCustom.csv')


    rCavs_df = pd.read_csv('data/rCavs.csv', sep = ',')
    rCavs_df = calc_sentiment_scores(rCavs_df, 'body')
    rCavs_df.to_csv('data/rCavsScored.csv')
    #generate with customized lexicon
    rCavs_df_custom = calc_sentiment_scores_custom(rCavs_df, 'body')
    rCavs_df_custom.to_csv('data/rCavsScoredCustom.csv')


    rDubs_df = pd.read_csv('data/rDubs.csv', sep = ',')
    rDubs_df = calc_sentiment_scores(rDubs_df, 'body')
    rDubs_df.to_csv('data/rDubsScored.csv')
    #generate with customized lexicon
    rDubs_df_custom = calc_sentiment_scores_custom(rDubs_df, 'body')
    rDubs_df_custom.to_csv('data/rDubsScoredCustom.csv')
    