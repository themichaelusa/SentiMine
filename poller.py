
"""
from newsapi.sources import Sources
s = Sources(API_KEY=key)


from newsapi.articles import articles

a = Articles(API_KEY=key)
popular = a.get_by_popularity()
"""

NEWS_API_HEADLINES = "https://newsapi.org/v2/top-headlines?q="
NEWS_API_KEY_QUERY = "&apiKey="

import requests
import json

def getArticles(keyword):
	url = NEWS_API_HEADLINES + keyword + NEWS_API_KEY_QUERY + key
	data = requests.get(url).json()
	print(data)

getArticles("Infrastructure")

