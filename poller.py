import grequests
import datetime
import json

class Poller:
	def __init__(self, apikey):
		self.apikey = apikey
		self.NEWS_API_HEADLINES = 'https://newsapi.org/v2/top-headlines?q={}&sources={}'
		self.NEWS_API_KEY_QUERY = "&pageSize=100&sortBy=relevancy&apiKey=" + apikey

	def getArticles(self, keywords, sources):
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		source_str = ','.join(sources)
		urls = [self.NEWS_API_HEADLINES.format(kwd, source_str) + 
			self.NEWS_API_KEY_QUERY for kwd in keywords]
		
		rs = (grequests.get(u, timeout=2) for u in urls)
		data = grequests.map(rs)
		return [d.json() for d in data if d is not None]

"""
from constants import fin_sources
p = Poller('foobar')
print(p.getArticles(['AMD', 'trump'], fin_sources))
"""
