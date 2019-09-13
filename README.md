# Senitment vs Excitement
#### Analyzing real-time reactions to Game 7 of the 2016 NBA Finals

## Motivation:
To most NBA fans, the 2016 Finals was one of the most legendary playoff series of all time. The Cleveland Cavaliers, led the greatest player on the planet, Lebron James, squared off against defending champions and regular season record setting Golden State Warriors, starring soon-to-be back-to-back league MVP Steph Curry. It's hard to overstate the hype going into the series and it delivered in every way. The underdog Cavs eventually won in 7 games after being down 3-1, a first for an NBA final series. Fans everywhere went wild. 

But how wild? And who did? Can we determine, quantatatively, the excitement of Cavaliers fans when the finally ended their city's 52 year championship drought? What about the disappointment of Warriors fans for not finishing a near perfect season? Can we guage the reaction of fans across the world when [the block heard around the world](https://youtu.be/wgVOgGLtPtc?t=177) happened?

Let's try and find out.

## Data:
Thanks to social media platforms and their APIs it's easy to collect data about big events. For this project, using user activity from either Reddit and Twitter was considered. In the end Reddit comments were used for a few reasons

  **1)** Structure: the comment-board design of reddit is much less chaotic than Twitter. Also, determining a commenters' team    allegiance is much easier thanks to user flair and teams having individual subreddits which was critical for this analysis
  
  **2)** The team at pushshift.io has a [public database](https://files.pushshift.io/reddit/comments/) of the entire history of reddit comments. Creating the datasets was made even easier thanks to the fact this database has been uploaded to [Google Big Query](https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments). Thanks to this, a simple query using the comment thread link IDs and subreddit name gave the exact table that was desired and could be downloaded in a .csv format. 
  
  **3)** I spend a lot (too much?) time on reddit so the platform is familiar.
 


 With the data sets imported, further filtering was done with python's Pandas library. Five datasets were created and used from "game threads" (threads posted by moderators for users to live-comment on games as they happen).
 
 * All comments from the main r/NBA game thread
 * All comments from the r/Cavaliers game thread
 * All comments from the r/Warriors game thread
 * Comments from the r/NBA game thread with Cavaliers flair (a user selected icon to indicate team allegiance)
 * Comments from the r/NBA game thread with Warriors flair

 Each comment was scored on it's sentiment using the `Afinn()` library. This uses a machine-learning-generated lexicon of over 3000 words and a value indicataing thier positive/negative connotation (e.g. happy = 3, sad = -2). Each comment assigned a score, the sum of all word values that appear in the lexicon (e.g. the comment 'happy sad' would have a score of 1).
 
 Each of these datasets were then filtered to capture the same time period (2 hours and 45 minutes from the start of the broadcast) then binned it could be analyzed in 'slices' over this time range. This binning was helpful because
 
 * It helped gauge sentiment for chunks of comments
 * Reactions can be delayed because of broadcast delay, not being able to comment exactly when something exciting happens, etc.
 * Enabled looking at comment density/frequency over time
 
 For most of this analysis, 50 bins were used, translating to roughly 3.3 minutes per chunk (2hr 45min = 9900 secs, 9900sec/50 bins = 198 secs/bin = 3.3 min/bin). This number, 50, was used because it was easy to remember while working on multiple scripts at once and translated to nice, digestible plots. 3.3 minutes might not be the friendliest time period, however several reasonable numbers of bins, translating from 1 to 5 minute chunks, were tested and the results were largely the same.

 
 ## Analysis Part 1
 

The main goal of this analyis was to look at trends of comment sentiment and frequency. Simple line plots of these quantaties over time are perfect for something like this.

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/MeanScoreCommentDensityDefault.png "main")

Overall, there is an overall negative sentiment in these comments (but keep this in mind for Part 2). All of the density plots show an increase in comments over the course of the game and a giant spike towards the end. This makes makes sense with how dramatic of a finish the game had. There appears to be some degree of correlation between Cavs fans in their own subreddit and in the r/NBA thread in terms of both sentiment and comment density. It's interesting that Warriors fans didnt demonstrate a similar pattern.

Originally one of the main goals of this analysis was to see if significant in-game events could be identified in these plots. Because scoring data only records in game timestamps and not "real world" time, this wasn't possible for the scope of this analysis. However, examining the raw data, plays like ["the block"](https://youtu.be/wgVOgGLtPtc?t=177) that happens around time = 45 can be identified by cross-referencing the binned data and the plot.

Although it doesn't result in much more insight, here is all of the plots for each sentiment and density overlaid one another.

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/MeanScoreOverlap.png "overlap scores")
![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/CommentDensityOverlap.png "overlap densities")



To the quantify correlations that appear to show in these plots, a correlation heatmap was generated

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/Correlation.png "heatmap")

* There's a clear negative correlation between density and sentiment illustrated by the distinct quadrants of orange/yellow and purple/pink.
* There's higher correlation of sentiment between r/NBA comments and comments from Cavs fans (based on subreddit and flair) than for Warriors fans. This might indicate more neutral fans were supporting the Cavaliers, which from anecdotal evidence was the case.


## Analysis Part 2: The F-Bomb

The overall negative sentiment was alluded to before. This was obvious at first glance of the dataset of comments because...  

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/WordCloudCensored.png "wordcloud")

This is a word cloud of all the words that appear in the comments which are scored in `Afinn()`. The 'f-bomb' and most of it's variations have a score of -4, and with the volume of which it appears in the comments, skews the sentiment data negatively extremely hard.

This is inaccurate to reality. An "f-yeah LeBron!" in real life would be considered a positive reaction, but that comment would get scored as a -4.

Luckily, editing python libraries is very easy. A copy of the library was made and the two biggest words from this word cloud were removed. This is how that simple edit changed the look of our sentiment plot

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/CommentDensityCustomAfinn.png "defaultvcustomafinn")

A hypothesis test for the difference in means on this data was performed, giving **p-val = 0.003**, which is significant at any reasonable alpha value and degrees of freedom

