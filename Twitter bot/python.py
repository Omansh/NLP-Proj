# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:15:33 2019

@author: omans
"""


#Importing the libraries
import tweepy
import re
import pickle
from tweepy import OAuthHandler #will be used for the authentication of our client machine with twiiter server. 


#Initializing the keys
consumer_key = 'place your key here'
consumer_secret = 'place your key here'
access_token = 'place your key here'
access_secret = 'place your key here'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
args = ['facebook']
api = tweepy.API(auth, timeout=10)

list_tweets=[]

query = args[0]
if len(args)==1:
    for status in tweepy.Cursor(api.search, q=query+" -filter:retweets", lang='en', result_type='recent').items(100):
        list_tweets.append(status.text)
        
        

#Loading the TF-IDF MODEL & Classifier
with open ('tfidfmodel.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
    
with open('classifier.pickle', 'rb') as f:
    clf = pickle.load(f)
    
    
total_pos=0
total_neg=0
    
#Testing the clasisfier
clf.predict(vectorizer.transform(['You are a nice person man, have a good life']))
    
for tweet in list_tweets:
    tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    tweet = re.sub(r'\s+https://t.co/[a-zA-Z0-9]*\s', " ", tweet)
    tweet = re.sub(r's+https://t.co/[a-zA-Z0-9]*$', " ", tweet)
    tweet = tweet.lower()
    tweet = re.sub(r"that's", "that is", tweet)
    tweet = re.sub(r"there's", "there is", tweet)
    tweet = re.sub(r"what's", "what is", tweet)
    tweet = re.sub(r"where's", "where is", tweet)
    tweet = re.sub(r"she's", "she is", tweet)
    tweet = re.sub(r"He's", "He is", tweet)
    tweet = re.sub(r"can't", "can not", tweet)
    tweet = re.sub(r"shouldn't", "could not", tweet)
    tweet = re.sub(r"can't", "can not", tweet)
    tweet = re.sub(r"couldn't", "could not", tweet)
    tweet = re.sub(r"would't", "would not", tweet)
    tweet = re.sub(r"won't", "will not", tweet)
    tweet = re.sub(r"\W", " ", tweet)
    tweet = re.sub(r'\d', ' ', tweet)
    tweet = re.sub(r"s+[a-z]\s+", " ", tweet)
    tweet = re.sub(r"\s+[a-z]$", " ", tweet)
    tweet = re.sub(r"^[a-z]\s+", " ", tweet)
    tweet = re.sub(r"\s+", " ", tweet)
    sent=clf.predict(vectorizer.transform([tweet]).toarray())
    if sent[0]==1:
        total_pos += 1
    else:
        total_neg += 1
        

#Plotting the result
import matplotlib.pyplot as plt
import numpy as np
objects = ['Positive', 'Negative']
y_pos=np.arange(len(objects))  
plt.bar(y_pos, [total_pos, total_neg], alpha=0.5)
plt.xticks(y_pos, objects)
plt.title("Number of positive and negative tweets")

plt.show()
