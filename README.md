# Senitment vs Excitement

### Analyzing Real-Time Reactions to Game 7 of the 2016 NBA Finals
##### By Lucas Xavier Churchman

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/Banner.png "banner")

## Table of Contents
1. [Motivation](#motivation)
2. [Data](#data)
4. [Analysis](#analysis)
5. [Takeaways](#takeaways)
6. [Credits and Acknowledgements](#credits-and-acknowledgements)

## Motivation:
To most NBA fans, the 2016 Finals was one of the most legendary playoff series of all time. The Cleveland Cavaliers, led by the greatest player on the planet, Lebron James, squared off against defending champions and regular season record setting Golden State Warriors, starring soon-to-be back-to-back league MVP Steph Curry. It's hard to overstate the hype going into the series and it end up delivering in every way. The underdog Cavs eventually won the series in 7 games after being down 3-1, a first for an NBA final series. Fans everywhere went wild. 

But how wild? And who did? Can we determine, quantatatively, the excitement of Cavaliers fans when their city's 52 year championship drought finally came to an end? What about the disappointment of Warriors fans for not capping off a near perfect season? Can we gauge the reaction of fans across the world when [the block heard around the world](https://youtu.be/wgVOgGLtPtc?t=177) happened?

Let's try and find out.

## Data:
For this project, using comments/tweets from either Reddit or Twitter was considered. In the end, Reddit comments were used for a few reasons.

  * Structure: the comment-board design of reddit is easier to follow than Twitter's handling of tweets and their reply threads. Also, determining a commenters' team allegiance is much easier thanks to user flair and teams having individual subreddits, both of which turned out to be critical for this analysis.
  
  * The team at pushshift.io has a [public database](https://files.pushshift.io/reddit/comments/) of the entire history of reddit comments. Creating the datasets was made even easier thanks to the fact this database has been uploaded to [Google Big Query](https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments). Thanks to this, a simple query using a thread's link IDs and subreddit name gave the exact table that was desired and could be downloaded in a .csv format. 
  
  * I spend a lot (too much?) time on reddit so the platform is familiar.
 


 With the data sets imported, further filtering was done using Python's Pandas library. Five datasets were created and used from 3 "game threads" (threads posted by subreddit moderators for users to live-comment on games as they happen). These datasets contained:
 
 * All comments from the main r/NBA game thread
 * All comments from the r/Cavaliers game thread
 * All comments from the r/Warriors game thread
 * Comments from the r/NBA game thread with Cavaliers flair (a user selected icon to indicate team allegiance)
 * Comments from the r/NBA game thread with Warriors flair

 Each comment was assigned a 'sentiment score' using the `Afinn()` library. This uses a machine-learning-generated lexicon of over 3000 words and values indicataing their positive/negative connotation (e.g. happy = 3, sad = -2). Each comment was assigned a score; the sum of all word values that appear in the lexicon (e.g. the comment 'happy sad' would have a score of 1).
 
 Each of these datasets were then filtered to capture the same time period (2 hours and 45 minutes from the start of the broadcast at 8pm EST, capturing comments a few minutes before tip-off and a few minutes after the game ended) and then binned so it could be analyzed in 'slices' over this time range. This binning was critical because:
 
 * It helped gauge general user sentiment in periods of time rather than per user comment.
 * Reactionary comments can be delayed because of broadcast delay, not being ready to comment the exact moment something exciting happens, etc.
 * It enabled looking at comment 'density' over time.
 
 For most of this analysis, 50 bins were used, translating to roughly 3.3 minutes per slice (2hr 45min = 9900 secs, 9900sec/50 bins = 198 secs/bin = 3.3 min/bin). This number, 50, was used because it was easy to remember while working between multiple scripts at once and translated to nice, digestible plots. 3.3 minutes might not be the friendliest time period to remember, however several reasonable numbers of bins, translating to slices of time ranging from 1 to 5 minutes, were tested and the results of the analysis were largely the same.

 ## Analysis
 ### Part 1: Sentiment and Density
 
With the data prepared, line plots were simple enough to generate and give a perfect visual idea of what's of interest.

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/SentimentScoreCommentDensityDefault.png "main")

* Overall, there is an overall negative trend of sentiment in these comments (keep this in mind for Part 2). All of the density plots show an increase in comment frequency over the course of the game and a giant spike towards the end, which makes sense with how dramatic of a finish the game had. There appears to be a moderate degree of correlation between Cavs fans in their own subreddit and flaired fans in the r/NBA thread both in terms of sentiment and comment density. It's interesting that Warriors fans didnt demonstrate a similar pattern.

* Originally one of the main goals of this analysis was to see if significant in-game events could be identified in these plots. Because NBA game data only records in game timestamps and not "real world" time, this wasn't possible for the scope of this analysis. However, plays like ["the block"](https://youtu.be/wgVOgGLtPtc?t=177) can be identified at time = 45  by cross-referencing the .csv of the binned data and this plot.

* Although it doesn't result in much more insight, here are all of the plots for both sentiment and density overlaid one another.

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/SentimentScoreOverlap.png "overlap scores")
![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/CommentDensityOverlap.png "overlap densities")

To the quantify correlations that appear to show in these plots, a correlation heatmap was generated

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/Correlation.png "heatmap")

* There's a clear postive correlations for sentiments and densities with themseleves and negative correlations between densities and sentiments, illustrated by the distinct quadrants of orange/yellow vs. purple/pink.
* Higher correlation in sentiment between r/NBA comments and comments from Cavs fans (based on subreddit and flair) than for Warriors fans. This might indicate more neutral fans were supporting the Cavaliers, which from anecdotal evidence was the case in reality.

### Part 2: The F-Bomb

The overall negative sentiment was alluded to before. This was obvious at first glance of the dataset of comments. To better demonstrate this, a word cloud was generated from a list of all the words found in the comments that are scored in `Afinn()`. The bigger the word, the more it appeard in comments

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/WordCloudCensored.png "wordcloud")

Yikes. The 'f-bomb' and most of it's variations have a score of -4, and the volume of which it appearsskews the sentiment data negatively **extremely** hard.

Luckily, editing python libraries is very easy. A copy of the library was made and the two biggest words from this word cloud were removed from the scoring lexicon. This is how that simple edit changed the look of our sentiment plot

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/SentimentScoreCustomAfinn.png "defaultvcustomafinn")

The mean sentiment increased from -0.21 to 0.11 for our 45,269 comment. A hypothesis test for the difference in means of this data was performed, giving **p-val = 0.000002**, which is significant at any reasonable alpha value.

These results are dramatic and should be taken with a grain of salt. Before editing the lexicon, an "f-yeah LeBron!" in real life would be considered a positive reaction, but that comment would get scored as a -4. On the other hand, an "f-you Lebron!" is a negative reaction and really should be scored as a -4. However, both these examples with our new lexicon would be scored 0.

The point here is that our sentiment analysis fails to account for one very important thing: context.

## Takeaways
Although this analysis evolved away from what it originally set out to discover, plenty else was discovered in its place. Predicted trends of comment density between different indicators of fandom appeared in the plots and calculations. The same goes for sentiment although less-so. As a bonus, some degree of an inverse correlation between comment density and sentiment was shown, but the reasons for this are unclear.

Furthermore, the 2nd part of the analysis displayed just how important context is for analyzing text, especially when gauging sentiment. Instant, reactionary comments on social media are fundamentally different from well thought out response to, say, an email survey or product review. This opens the door for future projects that take this into account, possibly utilizing this knowledge of some inverse correlation between sentiment and comment density.

## Credits and Acknowledgements

* Reddit user /u/Stuck_In_the_Matrix and the rest of the Pushshift.io team for their Reddit comment database
* Reddit user /u/fhoffa for uploading this database to Google Big Query
* The creators of the `Afinn()` library, along with the requested citation in their repo's readme:

 Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs", Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages. Volume 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)
