import numpy as np 
import pandas as pd 
from afinn import Afinn

af = Afinn(emoticons=True)

def combineDFs(list_of_dfs):
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
        df = df.append(data_frame)
    return df

def convertUTC(df, epoch_time_col_name, new_col_name):
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

def calcSentimentScores(df, comment_text_col_name):
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

def createTimeBins(df, n_bins = 1000):
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

def binDfs(listDFs):
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
    cols_wanted = ['created_utc','sentiment_score','score','author','author_flair_css_class','body']
    binned_dfs = []
    for i, df in enumerate(listDFs):
        df = df[cols_wanted]
        df = convertUTC(df, 'created_utc', 'created_utc_dt')
        df = df[(df['created_utc_dt'] >= '2016-06-20 00:00:00') & (df['created_utc_dt'] <= '2016-06-20 02:45:00')]
        df = createTimeBins(df, n_bins = 50) 
        binned_dfs.append(df)

    return [binned_dfs[x] for x in range(len(binned_dfs))]
    

if __name__ == "__main__":
    df1 = pd.read_csv('data/rNBA1stHalf.csv', sep = ',')
    df2 = pd.read_csv('data/rNBA2ndHalf.csv', sep = ',')
    rNBA_dfs = [df1, df2]
    rNBA_df = combineDFs(rNBA_dfs)
    rNBA_df = calcSentimentScores(rNBA_df, 'body')
    rNBA_df.to_csv('data/rNBACombinedScored.csv')

    rCavs_df = pd.read_csv('data/rCavs.csv', sep = ',')
    rCavs_df = calcSentimentScores(rCavs_df, 'body')
    rCavs_df.to_csv('data/rCavsScored.csv')

    rDubs_df = pd.read_csv('data/rDubs.csv', sep = ',')
    rDubs_df = calcSentimentScores(rDubs_df, 'body')
    rDubs_df.to_csv('data/rDubsScored.csv')
    