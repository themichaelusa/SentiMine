import grequests
import datetime
import json

class Poller:
	def __init__(self, apikey, init_keywords):
		self.apikey = apikey
		self.init_keywords = [ik.lower() for ik in init_keywords] 
		self.NEWS_API_HEADLINES = 'https://newsapi.org/v2/top-headlines?q={}&sources={}'
		self.NEWS_API_KEY_QUERY = "&pageSize=100&sortBy=relevancy&apiKey=" + apikey

	def get_articles(self, keywords, sources):
		# prepare/format urls
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		source_str = ','.join(sources)
		keywords = [k.lower() for k in keywords]
		keywords.extend(self.init_keywords)
		urls = [self.NEWS_API_HEADLINES.format(kwd, source_str) + 
			self.NEWS_API_KEY_QUERY for kwd in set(keywords)]
		
		# get news api data in parallel
		rs = (grequests.get(u, timeout=2) for u in urls)
		data = grequests.map(rs)
		data_json = [d.json() for d in data if d is not None]
		
		# get all descriptions for each src for each kwd
		all_descs = []
		for kwd_dict in data_json:
			kwd_descs = []
			for article in kwd_dict['articles']:
				src = article['source']['id']
				desc = str(article['description']).lower()
				kwd_descs.append((src, desc))
			all_descs.append(kwd_descs)

		# match descriptions with keywords
		data_formatted = {k: [] for k in keywords}
		for kwd_descs in all_descs:
			next_desc = False
			for src, desc in kwd_descs:
				for k in keywords:
					if desc.find(k) != -1:
						data_formatted[k] = kwd_descs
						next_desc = True
						break
				if next_desc:
					break

		return data_formatted

# (TEST poller.py)
"""
from constants import fin_sources
p = Poller('blah', [])
print(p.get_articles(['AMD', 'trump'], fin_sources))
"""
