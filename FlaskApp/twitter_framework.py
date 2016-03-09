import twitter
import json
from geopy.geocoders import Nominatim

consumer_key = 'OhCetqrIfnOpAklUngIPe9SRO'
consumer_secret = 'AIN2M9MZg0egiXE5P5bJM2vsZPwp79hCjMgbnrTfvLvEQoEC9f'
oauth_token = '695168737662603264-Cw5UkEVceQbh3cugKMIzprepaPtNMdg'
oauth_secret = 'ZSHhT1lnwCkQDxwPr3hh64WXIDfZKMYOlfTxDEXkttwlx'
auth = twitter.oauth.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID) # get back a callable
#print world_trends

def retrieve_tweets(q, count=100):
	search_results = twitter_api.search.tweets(q=q, count=count)
	statuses = search_results['statuses']

	return statuses


def get_geo_location(user_location):
	geolocator = Nominatim()
	try:
		location = geolocator.geocode(user_location)
		if location != None:
			return (location.latitude, location.longitude)
	except:
		return None


def extract_tweets(query):
	statuses = retrieve_tweets(query)
	result = [{'location':get_geo_location(status['user']['location']), 
			   'message':status['text'], 'timestamp':status['created_at']} for status in statuses]

	return result