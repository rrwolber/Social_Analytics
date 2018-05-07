# Social_Analytics


While running, @RWplotbot bot receives tweets via mentions and in turn performs sentiment analysis on the most recent twitter account specified in the mention. For example, when a user tweets, "@RWplotbot Analyze: @CNN," it will trigger a sentiment analysis on the CNN twitter feed. Example sentiment analysis graphs attached as PNGs. 

RWplotbot utilizes twitter API to analyze the 150 most recent, unique tweets (excludes retweets) and runs tweet text through Vader sentiment analysis, plotting overall sentiment score through matplotlib.
