import grequests
import datetime
import json

class Poller:
	def __init__(self, apikey, keywords):
		self.apikey = apikey
		self.keywords = keywords
		#self.NEWS_API_HEADLINES = "https://newsapi.org/v2/top-headlines?country=us&q={}&language=en"
		self.NEWS_API_EVERYTHING = "https://newsapi.org/v2/everything?q=+{}&langauge=en"
		self.NEWS_API_DATES = "&from={}&to={}"
		self.NEWS_API_KEY_QUERY = "&pageSize=100&sortBy=relevancy&apiKey=" + apikey
		#self.NEWS_API_KEY_QUERY = "&apiKey=" + apikey

	def getArticles(self):
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		url = self.NEWS_API_DATES.format(today, today) + self.NEWS_API_KEY_QUERY
		urls = [self.NEWS_API_EVERYTHING.format(kwd) + url for kwd in self.keywords]
		rs = (grequests.get(u, timeout=.05) for u in urls)
		data = grequests.map(rs)
		extract = [d.json() for d in data if d is not None]
		print(extract)


