# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 12:38:13 2021

@author: Matija
"""

import discord
import time
import tweepy
from Twitter_sentiment import scrape, save_photo
import nest_asyncio
nest_asyncio.apply()

# PLUG IN YOUR INFO HERE (PREFERENCES)
########################################
# Twitter connection
# Replace with your credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Discord connection
# Replace with your own connection
discord_key = ''

# Filenames for saving tweets and tweet sentiment
tweets_file = 'scrapped_tweets.csv'
sentiment_file = 'sentiment_at_datetime.csv'
plot_name = 'Sentiment_at_datetime.png'

# Sleep time
sleep_time = 600
# Keywords
keyword = 'bitcoin'
# Number of tweets to analyze
numtweet = 1000
########################################

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # After running programme type $run into discord server to run
    if message.content.startswith('$run'):
        while True:
            datetime, sentiment = scrape(words=keyword, numtweet=numtweet, api=api, tweets_file=tweets_file,sentiment_file=sentiment_file)
            save_photo(sentiment_file=sentiment_file, plot_name=plot_name)
            await message.channel.send(f'Datetime: {datetime}, Sentiment: {sentiment}', file=discord.File(plot_name))
            time.sleep(sleep_time)

client.run(discord_key)