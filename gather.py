from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import gzip
import os
import codecs

# create following tokens at apps.twitter.com
ckey = ""
csecret=""
atoken=""
asecret=""

# setup listener
file_format ="%Y%m%d-%H%M%S"
directory_format="%Y%m%d"
counter = 0
f=None
class listener(StreamListener):
	def on_data(self, data):
		if (counter == 0):
			global counter
			counter = 1000
			if (f is not None):
				f.close()
			dir_name = time.strftime(directory_format)
			if not os.path.exists(dir_name):
				os.makedirs(dir_name)
			timestr = time.strftime(file_format)
			global f
			f = gzip.open(dir_name + '/' + timestr + '.txt.gz', 'wb')
		counter = counter - 1
		f.write(data)
		#print(data)

#https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
#	def on_status(self, status):
		#print(status.text)
		
	def on_error(self, status):
		print(status)
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

while True:
	try:
		twitterStream = Stream(auth, listener())
		keywords_file = codecs.open('keywords.txt', 'r',encoding='utf8')
		keywords = keywords_file.read().split(',')
                for v in keywords:
                    print("v="+v)
                twitterStream.filter(track=keywords, languages=["ko"], stall_warnings=True)
		break

	except Exception,e:
		print("oops try again,,"+str(e))
	counter=0
	time.sleep(5) #delay 5 seconds
