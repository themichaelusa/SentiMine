import analysis 
import poller 

if __name__ == '__main__':

	### FLASK API INIT ###
	import api 

	### POSTGRES DB INTEGRATION ###


	### PARSE CONFIG.TXT FILE ###
	import sys
	file = open(sys.argv[1], 'r')	
	key, init_keywords = "", []
	for line, idx in enumerate(file.readlines()):
		if idx == 0:
			key.join(line)
		else:
			init_keywords.append(line)

	### INSTANCE CREATION ###
	sa = analysis.SentimentAnalysis()
	ta = analysis.TopicAnalysis()
	p = Poller(key, init_keywords)
	from constants import fin_sources

	while: pass
		### CHECK IF SCRAPING VALID ###

		### SCRAPE NEWS FROM SOURCES LIST ###
		# pull kwds from db
		keywords = []
		# pass into poller 
		all_kwds, data = p.get_articles(keywords, fin_sources)

		### PERFORM SENTIMENT ANALYSIS ###
		sa_data = sa.get_group_polarity(all_kwds, data)
		### PERFORM TOPIC ANALYSIS ###
		ta_data = 






