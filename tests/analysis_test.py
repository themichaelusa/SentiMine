import poller
import analysis 
from constants import fin_sources

if __name__ == '__main__':

	doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
	doc2 = "My father spends a lot of time driving my sister around to dance practice."
	doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
	doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
	doc5 = "Health experts say that Sugar is not good for your lifestyle."
	doc_complete = [doc1, doc2, doc3, doc4, doc5]

	p = poller.Poller('blah', [])
	data = p.get_articles(['AMD', 'trump'], fin_sources)

	ta = analysis.TopicAnalysis()
	print(ta.group_mine_topics(data))

	sa = analysis.SentimentAnalysis()
	print(sa.get_group_polarity(data))