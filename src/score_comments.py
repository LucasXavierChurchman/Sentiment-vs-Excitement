import numpy as np 
import pandas as pd 
from afinn import Afinn

af = Afinn(emoticons=True)

def score_data(list_of_dfs, cols_wanted, comment_text_col_name):
    '''Return appended data sets from list (can be a list of 1 data set) with 
    specified columns and calculates sentiment scores from column containing 
    the text strings of interest.

    Parameters
    ----------
    list_of_dfs: list of pandas dataframes
    cols_wanted: desired columns for returned df
    comment_text_col_name: name of the column with text strings to be scored

    Returns
    -------
    Pandas DataFrame
    '''

    df = list_of_dfs[0]
    for data_frame in list_of_dfs[1:]:
        df = df.append(data_frame)
    
    # sent_scores = []
    # for comment in df[comment_text_col_name]:
    #     try:
    #         sent_scores.append(af.score(comment))
    #     except:
    #         sent_scores.append(0)
    # df['sent_scores'] = sent_scores
    # df = df[cols_wanted]
    return df

if __name__ == "__main__":
    df1 = pd.read_csv('data/Game7-1stHalf.csv', sep = ',')
    df2 = pd.read_csv('data/Game7-2ndHalf.csv', sep = ',')
    dfs = [df1, df2]
    cols = ['created_utc', 'body', 'author','author_flair_css_class', 'ups']
    df = score_data(dfs, cols, 'body')
    

