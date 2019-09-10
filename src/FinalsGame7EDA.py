import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import prep_data

df = pd.read_csv('data/Game7CombinedWithSentScores.csv', sep = ',')

df = prep_data.convertUTC(df, 'created_utc')
df.head()

#Once converted into a more human-friendly time format, it shows the 'created_utc' column is off by
#several days and hours from when the comments were actually submitted. Not sure why this is,
#but we can visit the reddit thread to find the actual time the comment was submitted, calculate the 
#difference between that time and our 'created_utc' time, and apply that offset to the entire column



#looks some people were commenting in the thread days after the game was over. Lets fix that.
print(df.tail())
df = df[(df['timestamp'] < '2016-06-20 03:00:00')]


df = prep_data.createTimeBins(df, 1000)

data = df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
# x = np.linspace(0, data.shape[0], num = data.shape[0])

# fig, ax = plt.subplots(1, figsize=(16, 3))
# ax.plot(x, data['sentiment_score']['mean'])
# plt.show()
