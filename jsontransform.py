import json
import pandas as pd
import matplotlib as matplot
from textblob import TextBlob
import HTMLParser

tweets_data_path = '/Users/Starshine/goodlistener/clintontxt.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets_data
len(tweets_data)
tweets = pd.DataFrame()


'''
This is often the case with JSON generated
by the Twitter API that certain fields/keys will not be present for some tweets
Instead of :
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
Replace this with:
tweets['text'] = map(lambda tweet: tweet.get('text', None),tweets_data)'''

tweets['text'] = map(lambda tweet: tweet.get('text', None),tweets_data)
tweets['lang'] = map(lambda tweet: tweet.get('lang', None), tweets_data)
tweets['country'] = map(lambda tweet: tweet.get('place','country') if tweet.get('place') != None else None, tweets_data)


tweets
tweets.text[17]
x = TextBlob(tweets.text[17])
x.sentiment

def detect_sentiment(tweets):
    return TextBlob(tweets.text.sentiment.polarity)

# use `.apply` to create a new column where the value is the result of applying the function to the text
tweets['sentiment'] = tweets.text.apply(detect_sentiment)


#cleaning part
tweet = tweets.text[17]
tweet


#use this for now, removes 
y = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())

z = TextBlob(y)
z.sentiment
TextBlob(y)
html_parser = HTMLParser.HTMLParser()
def tweetclean(tweets):
    newtweet = html_parser.unescape(tweet)

tweetclean(tweet)
