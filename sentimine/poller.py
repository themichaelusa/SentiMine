#import grequests
import requests 
import datetime
import json

from multiprocessing.dummy import Pool as ThreadPool 
from itertools import chain 

class Poller:
	def __init__(self, apikey, init_keywords):
		self.apikey = apikey
		self.init_keywords = [ik.lower() for ik in init_keywords] 
		self.NEWS_API_HEADLINES = 'https://newsapi.org/v2/top-headlines?q={}&sources={}'
		self.NEWS_API_KEY_QUERY = "&pageSize=100&sortBy=relevancy&apiKey=" + apikey

		from constants import sources as all_srcs
		self.all_sources = list(chain(*all_srcs.values()))

	def __get_article(self, url_kwd):
		url, keyword = url_kwd
		return (keyword, requests.get(url).json())

	def get_articles(self, keywords, sources):
		# prepare/format urls
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		source_str = ','.join(sources)
		keywords = [k.lower() for k in keywords]
		keywords.extend(self.init_keywords)
		urls_kwds = [(self.NEWS_API_HEADLINES.format(kwd, source_str) + 
			self.NEWS_API_KEY_QUERY, kwd) for kwd in set(keywords)]
		
		#todo: replace grequests with with thread pool so we can actually track kwd searches

		# get news api data in parallel
		#all_reqs = (grequests.get(u, timeout=2) for u in urls)
		#data = grequests.map(all_reqs)
		#data_json = [d.json() for d in data if d is not None]

		pool = ThreadPool(8)
		data_json = pool.map(self.__get_article, urls_kwds)
		pool.close()
		pool.join()

		# todo: allow for multiple descriptions from same source, concat

		# get all descriptions for each src for each kwd
		print(data_json)
		all_descs = {}
		for kwd, kwd_dict in data_json:
			kwd_descs = {}
			for article in kwd_dict['articles']:
				src = article['source']['id']
				desc = str(article['description']).lower()
				kwd_descs[src] = desc

			#todo: add missing sources to dict to preserve consistency on user end 
			#missing = list(set(self.all_sources) - set(kwd_descs.keys()))
			#print(missing)
			all_descs[kwd] = kwd_descs

		print(all_descs)

	"""
	# match descriptions with keywords
	data_formatted = {k: [] for k in keywords}
	for kwd_descs in all_descs:
		next_desc = False
		for src, desc in kwd_descs.items():
			for k in keywords:
				if desc.find(k) != -1:
					data_formatted[k] = kwd_descs
					next_desc = True
					break
			if next_desc:
				break
	"""

		#return data_formatted