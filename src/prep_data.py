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

def convertUTC(df, unix_time_col_name):
    '''Uses a timestamp column w/ unix/epoch format to create a new one with 'normal' UTC timestamp format
      Parameters: 
    -----------
    df: dataframe with unix/epoch timestamp

    Returns
    -------
    Pandas DataFrame
    '''
    df['timestamp'] = pd.to_datetime(df[unix_time_col_name], unit='s')
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

def createTimeSlices(df, n_bins = 1000):
    df['time_slice'] = pd.cut(df['timestamp'], bins = n_bins, labels = range(n_bins))
    return df


if __name__ == "__main__":
    df1 = pd.read_csv('data/Game7-1stHalf.csv', sep = ',')
    df2 = pd.read_csv('data/Game7-2ndHalf.csv', sep = ',')
    dfs = [df1, df2]
    df = combineDFs(dfs)
    df = convertUTC(df, 'created_utc')
    n_slices = 10000
    df = createTimeSlices(df, n_slices)
    df = calcSentimentScores(df, 'body')
    df = df[['timestamp', 'created_utc', 'time_slice', 'sentiment_score','body','author','author_flair_css_class']]
    #looks some people were commenting in the thread days after the game was over. Lets fix that.
    df = df[(df['timestamp'] =< '2016-06-20 03:00:00')]
    df.to_csv('data/Game7CombinedWithSentScores'+str(n_slices)+'Slices.csv')

    

