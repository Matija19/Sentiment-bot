# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 13:59:20 2021

@author: Matija
"""


import pandas as pd
import tweepy
import time
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank
# import plotly.express as px
    
pos_list=set(opinion_lexicon.positive())
neg_list=set(opinion_lexicon.negative())

tokenizer = treebank.TreebankWordTokenizer()

# Replace with your credentials
consumer_key = "xxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxx"
access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxxxxxxxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def sentiment(sentence):
  senti=0
  words = [word.lower() for word in tokenizer.tokenize(sentence)]
  for word in words:
    if word in pos_list:
      senti += 1
    elif word in neg_list:
      senti -= 1
  return senti

def scrape(words, numtweet):
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags',
                               'created_at'], dtype=object)
    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    # print(f'{words} since: {date_since}')
    tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en",
                           tweet_mode='extended').items(numtweet)
    
    # .Cursor() returns an iterable object. Each item in 
    # the iterator has various attributes that you can access to 
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]
      
    # Counter to maintain Tweet Count
    i = 1  
    final_sentiment = 0
      
    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        created_at = tweet.created_at
          
        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
          
        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext,
                     created_at]
        db.loc[len(db)] = ith_tweet
          
        # Function call to print tweet data on screen
        # printtweetdata(i, ith_tweet)
        final_sentiment += sentiment(ith_tweet[7])
        i = i+1
    filename = 'scraped_tweets.csv'
      
    # we will save our database as a CSV file.
    db.to_csv(filename)

    filename = 'sentiment_at_datetime.csv'
    with open (filename, 'a') as fd:
        fd.write(f'\n{ith_tweet[9]},{final_sentiment}')
    
if __name__ == '__main__':
    while True:
        scrape('bitcoin', 100)
        time.sleep(120)
        

    
    

