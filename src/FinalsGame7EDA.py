import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


df = pd.read_csv('data/Game7CombinedWithSentScores10000Slices.csv', sep = ',')



data = df[['time_slice','sentiment_score']].groupby('time_slice').agg([np.mean, np.sum, np.size])
x = np.linspace(0, data.shape[0], num = data.shape[0])

fig, ax = plt.subplots(1, figsize=(16, 3))
ax.plot(x, data['sentiment_score']['mean'])
plt.show()
