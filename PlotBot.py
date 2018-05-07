import json
import tweepy
import pandas as pd 
import matplotlib.pyplot as plt 
import requests as req
import time
import numpy
import seaborn as sns
import numpy as np
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import apiInfo

analyzer = SentimentIntensityAnalyzer()
now = datetime.datetime.now()

# Twitter API Keys
consumer_key = 	apiInfo.key
consumer_secret = apiInfo.secret
access_token = apiInfo.token
access_token_secret = 	apiInfo.tokens

# Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),wait_on_rate_limit=True)

me = '@RWplotbot'
past_analyses = []  #formatted assuming bot were running forever
past_mentions = []
caller = ""

def MentionSentiment(user,ask):
    #compile sentiment list of last 500 tweets and return analysis with media

    oldest_tweet=0
    sentiments = []
    tweetcount = 0
    print(user)
    while tweetcount < 500:
        target_tweets = api.search(user, count=50,result_type='recent',max_id=oldest_tweet)

        # Loop through all tweets
        for tweet in target_tweets['statuses']:
            oldest_tweet = tweet['id_str']
            text = tweet["text"]
            tweetcount =tweetcount + 1
            print(tweetcount)


            # Run Vader Analysis on each tweet

            scores = analyzer.polarity_scores(text)

            sentiments.append(scores)

    sentiments_df = pd.DataFrame(sentiments)


    x_values = -1*(np.arange(len(sentiments_df)))
    y_values = sentiments_df["compound"]
    sns.set()
    at, = plt.plot(x_values,y_values,linestyle="-",linewidth=0.5, marker="o",label=f'{user}')
    plt.ylabel("Composite Sentiment Analysis (Vader)")
    plt.xlabel("Tweets Ago")
    plt.legend(handles=[at],title="Tweets",loc='upper left', bbox_to_anchor=(0.99, 1),prop={'size': 5})
    plt.xlim(-505,5)
    plt.ylim(-1.01,1.01)
    plt.title(f'Sentiment Analysis of Tweets ({now.month}/{now.day}/{now.year})')
    
    plt.savefig(f'Sentiment{user}.png', bbox_to_anchor=(0.99,1),prop={'size':5})
    plt.gcf().clear()
    api.update_with_media(f'Sentiment{user}.png', status=f'New Tweet Analysis: {user} (Thanks @{ask}!)')

    
while True:
    try:
        req = ""
        callerList = []
        reqList = []

        mentions = api.mentions_timeline()

        for mention in mentions:
            if mention["id"] not in past_mentions:
                caller = mention["user"]["screen_name"]
                past_mentions.append(mention["id"])
                if len(mention["entities"]["user_mentions"]) > 1:
                    req = f'@{mention["entities"]["user_mentions"][1]["screen_name"]}'
                    if req not in past_analyses:
                        past_analyses.append(req)
        
        MentionSentiment(req,caller)

    except tweepy.TweepError:
        time.sleep(1)
        


    time.sleep(5*60)
