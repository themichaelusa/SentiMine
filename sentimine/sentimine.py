
from constants import sources
from itertools import chain 

class SentiMine:
	def __init__(self, apikey, init_keywords=[]):
		import analysis 
		import poller as p
		self.sources = sources
		self.poller = p.Poller(apikey, init_keywords)
		self.sa = analysis.SentimentAnalysis()
		self.ta = analysis.TopicAnalysis()

	def __get_articles(self, keywords=[], news_type='all'):
		sources = None
		if news_type != 'all':
			sources = self.sources[news_type]
		else:
			sources = self.sources.values()
			sources = list(chain(*sources)) 

		return self.poller.get_articles(keywords, sources)

	def get_sentiment_dict(self, keywords=[]):
		data = self.__get_articles(keywords)
		return self.sa.get_group_polarity(data)

	def get_topic_dist(self):
		data = self.__get_articles(keywords)
		return self.ta.group_mine_topics(data)

"""
if __name__ == '__main__':
	s = SentiMine('bac1eed426c8416992bad5823b10a779')
	print(s.get_sentiment_dict(['AMD', 'trump', 'fed', 'russia', 'market', 'congress']))
	







	


		






