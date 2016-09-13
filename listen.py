import tweepy
import csv
import pandas as pd
from textblob import TextBlob, Word
from datetime import datetime

#Twitter API credentials
consumer_key = "Your Key"
consumer_secret = "Your Key"
access_key = "Your Key"
access_secret = "Your Key"


#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	pass
get_all_tweets("twitter")



#get tweets from a certain date range
def get_tweet_daterange(start_date,stop_date,screen_name):
	data = []
	tweets = api.user_timeline(screen_name=screen_name,count=200)
	while True:
		tweets_after_start = [tweet for tweet in tweets if tweet.created_at >= start_date]
		if len(tweets_after_start) == 0:
			break
		max_id = tweets_after_start[-1].id - 1
		data.extend(tweets_after_start)
		tweets = api.user_timeline(screen_name=screen_name,max_id=max_id,count=200)
	tweets = [[obj.user.screen_name.encode('utf-8'),obj.user.name.encode('utf-8'),obj.user.id,obj.user.description.encode('utf-8'),obj.created_at.year,obj.created_at.month,obj.created_at.day,"%s.%s"%(obj.created_at.hour,obj.created_at.minute),obj.id_str,obj.text.encode('utf-8')] for obj in data if obj.created_at <= stop_date ]
	dataframe=pd.DataFrame(tweets,columns=['screen_name','name','twitter_id','description','year','month','date','time','tweet_id','tweet'])
	dataframe.to_csv("%s_tweets.csv"%(screen_name),index=False)
#set the range of dates for the desired tweets
start_date  = datetime(2015,12,16)
stop_date  = datetime(2015,12,18)
get_tweet_daterange(start_date,stop_date, 'twitter')
