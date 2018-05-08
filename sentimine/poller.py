import grequests
import datetime
import json

import requests
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
		from multiprocessing import cpu_count
		self.cpu_count = cpu_count()

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

		pool = ThreadPool(self.cpu_count)
		data_json = pool.map(self.__get_article, urls_kwds)
		pool.close()
		pool.join()

		# todo: allow for multiple descriptions from same source, by pulling news 
		# for each day since some time in the morning 

		# get all descriptions for each src for each kwd
		all_descs = {}
		for kwd, kwd_dict in data_json:
			kwd_descs = {}
			for article in kwd_dict['articles']:
				src = article['source']['id']
				desc = str(article['description']).lower()
				kwd_descs[src] = desc
			all_descs[kwd] = kwd_descs

		return all_descs
