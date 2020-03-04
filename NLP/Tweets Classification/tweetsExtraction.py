###########################################################################
# Python script to extract tweets of Trump and Clinton official accounts
###########################################################################

import sys
from twython import Twython
import json
import pandas as pd
import numpy as np
import time
from datetime import date
from datetime import timedelta


with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

TrumpParams = {'screen_name': 'realDonaldTrump',
               'count': 200
               }
ClintonParams = {'screen_name': 'HillaryClinton',
                 'count': 200
                 }

with open("TrumpTweets.json", "r") as file:
    dict_T = json.load(file)
dict_T['user'] = list(dict_T['user'].values())
dict_T['date'] = list(dict_T['date'].values())
dict_T['text'] = list(dict_T['text'].values())
dict_T['favorite_count'] = list(dict_T['favorite_count'].values())
dict_T['id'] = list(dict_T['id'].values())
TrumpParams['max_id'] = int(min(dict_T['id'])) - 1
l = int(len(dict_T['user'])/1000) * 1000
while len(dict_T['user']) < l + 1000:
    for status in python_tweets.get_user_timeline(**TrumpParams):
        dict_T['user'].append(status['user']['screen_name'])
        dict_T['date'].append(status['created_at'])
        dict_T['text'].append(status['text'])
        dict_T['favorite_count'].append(status['favorite_count'])
        dict_T['id'].append(status['id'])
    TrumpParams['max_id'] = int(min(dict_T['id'])) - 1

# Structure data in a pandas DataFrame for easier manipulation
dfT = pd.DataFrame(dict_T)
dfT.sort_values(by='favorite_count', inplace=True, ascending=False)
Export = dfT.to_json(r'TrumpTweets.json')

with open("ClintonTweets.json", "r") as file:
    dict_C = json.load(file)
dict_C['user'] = list(dict_C['user'].values())
dict_C['date'] = list(dict_C['date'].values())
dict_C['text'] = list(dict_C['text'].values())
dict_C['favorite_count'] = list(dict_C['favorite_count'].values())
dict_C['id'] = list(dict_C['id'].values())
ClintonParams['max_id'] = int(min(dict_C['id'])) - 1

l = int(len(dict_C['user'])/1000) * 1000
while len(dict_C['user']) < l + 1000:
    for status in python_tweets.get_user_timeline(**ClintonParams):
        dict_C['user'].append(status['user']['screen_name'])
        dict_C['date'].append(status['created_at'])
        dict_C['text'].append(status['text'])
        dict_C['favorite_count'].append(status['favorite_count'])
        dict_C['id'].append(status['id'])
    ClintonParams['max_id'] = int(min(dict_C['id'])) - 1

# Structure data in a pandas DataFrame for easier manipulation
dfC = pd.DataFrame(dict_C)
dfC.sort_values(by='favorite_count', inplace=True, ascending=False)
Export = dfC.to_json(r'ClintonTweets.json')

# df = pd.concat([dfT, dfC], ignore_index=True)
# df_shuffled = df.reindex(np.random.permutation(df.index))

# Export = df.to_json(r'Tweets.json')
# Export = df_shuffled.to_json(r'Tweets_Shuffled.json')

# print(df.shape[0])  # debugging
