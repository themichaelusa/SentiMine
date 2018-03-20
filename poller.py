import grequests
import datetime
import json

class Poller:
	def __init__(self, apikey, init_keywords):
		self.apikey = apikey
		self.init_keywords = init_keywords
		self.NEWS_API_HEADLINES = 'https://newsapi.org/v2/top-headlines?q={}&sources={}'
		self.NEWS_API_KEY_QUERY = "&pageSize=100&sortBy=relevancy&apiKey=" + apikey

	def get_articles(self, keywords, sources):
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		source_str = ','.join(sources)
		keywords.extend(self.init_keywords)
		urls = [self.NEWS_API_HEADLINES.format(kwd, source_str) + 
			self.NEWS_API_KEY_QUERY for kwd in set(keywords)]
		
		rs = (grequests.get(u, timeout=2) for u in urls)
		data = grequests.map(rs)
		data_json = [d.json() for d in data if d is not None]

		data_formatted = []
		for kwd_dict, kwd in zip(data_json, keywords):
			for article in kwd_dict['articles']:
				src = article['source']['id']
				data_formatted.append((kwd, src, article['description']))

		return keywords, data_formatted

"""
from constants import fin_sources
p = Poller('blah')
print(p.get_articles(['AMD', 'trump'], fin_sources))
"""
