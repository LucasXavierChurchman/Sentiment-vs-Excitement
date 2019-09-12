# Senitment vs Excitement
#### Analyzing real-time reactions to Game 7 of the 2016 NBA Finals

## Motivation:
To most fans of the NBA, the 2016 Finals was one of the most legendary playoff series of all time. The Cleveland Cavaliers, led the greatest player on the planet Lebron James, squared off against defending champions and regular season record setting Warriors, starring soon-to-be back to back league MVP Steph Curry. It's hard to overstate the hype going into the series and it delivered in every way. The underdog Cavs eventually won in 7 games after being down 3-1, a first for an NBA final series. Sports fans everywhere went wild. 

But how wild? And who did? Can we determine, quantatatively, the excitement of Cavaliers fans when the finally ended their city's 52 year championship drought? What about the disappointment of Warriors fans for not finishing a near perfect season? Can we guage the reaction of fans across the world when [the most legendary block in NBA history](https://youtu.be/wgVOgGLtPtc?t=177) happened?

Let's try and find out.

## Data:
Thanks to social media platforms and their APIs it's easy to collect data about big events. For this project, using user activity from either Reddit and Twitter was considered. In the end Reddit comments were used for a few reasons

  **1)** Structure: the comment-board design of reddit is much less chaotic than Twitter. Also, determining a commenters' team    allegiance is much easier thanks to user flair and teams having individual subreddits which was critical for this analysis
  
  **2)** The team at pushshift.io has a [public database](https://files.pushshift.io/reddit/comments/) of the entire history of reddit comments. Creating the datasets was made even easier thanks to the fact this database has been uploaded to [Google Big Query](https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments). Thanks to this, a simple query using the comment thread link IDs and subreddit name gave the exact table that was desired and could be downloaded in a .csv format. From there, further filtering was done with python's pandas library.
  
  **3)** I spend a lot (too much?) time on reddit so the platform is very familiar.
 
 Five datasets were created and used from the game 7 "game threads" (threads posted by moderators for users to live-comment on games as they happen)
 
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
 

The main goal of this analyis was to look at trends of comment sentiment and frequency. Simple line graphs are perfect for something like this (opening these images in a new tab helps read them without loss of visual information/granularity)

![alt text](https://github.com/LucasXavierChurchman/Capstone1/blob/master/images/MeanScoreCommentDensityDefault.png "main")

Overall, there is an overall negative sentiment in these comments (but keep this in mind for Part 2). All of the density plots show an increase in comments over the course of the game and a giant spike towards the end. This makes makes sense with how dramatic of a finish the game had. There appears to be some degree of correlation between Cavs fans in their own subreddit and in the r/NBA thread in terms of both sentiment and comment density. It's interesting that Warriors fans didnt demonstrate a similar pattern.

Although it doesn't result in much more insight, here is all of the plots for each sentiment and density overlaid one another.



## 
