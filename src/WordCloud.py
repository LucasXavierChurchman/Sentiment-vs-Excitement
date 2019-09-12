'''
This entire thing is super inefficient/unorganized but I just wanted to have 
it in time for presentation
'''

from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from itertools import islice
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
plt.style.use('seaborn-darkgrid')

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

df  = pd.read_csv('data/rNBACombinedScored.csv', sep = ',', low_memory = False)
word_counts = df.body.str.split(expand=True).stack().value_counts()

comments = list(df.body)

afinn_table = pd.read_csv('etc/AFINN-en-165.csv', sep = '\t')
afinn_table.columns = ('words','val')
afinn_words = list(afinn_table.words)

words_of_interest = []
for comment in comments:
  comment = str(comment)
  words = comment.split(' ')
  for word in words:
    if word in afinn_words:
      words_of_interest.append(word)

counts = Counter(words_of_interest)
print(counts)

# Create and generate a word cloud image:
fig, ax = plt.subplots(figsize=(20,30))
wordcloud = WordCloud(background_color = 'white').generate(' '.join(words_of_interest))
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()