
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from itertools import chain
from nltk import tokenize

adjTags = ["JJ", "JJR", "JJS"]
nounTags = ["NN", "NNS", "NNP"]
verbTags = ["VBD", "VBG", "VBN", "VBP", "VBZ"]

def findSynonym(word):
	synonyms = wordnet.synsets(word)
	lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
	return list(lemmas)

class TopicAnalysis:
	def __init__(self):
		import gensim
		self.dictionary = gensim.corpora.Dictionary
		self.lda = gensim.models.ldamodel.LdaModel

	def tokenize(self, text):
		sentences = text.split('\n')
		words = [sent.split(" ") for sent in sentences]

		# flatten words list & apply lowercase 
		import itertools
		words = list(itertools.chain(*words))
		words =  [word.lower() for word in words]

		# import stopwords, punctuation corpora
		from nltk.corpus import stopwords 
		from nltk.stem.wordnet import WordNetLemmatizer
		from string import punctuation

		# remove punctuation
		punc = set(punctuation)
		all_chars = [list(word) for word in words]
		no_punc = []
		for char_list in all_chars:
			no_punc.append("".join([c for c in char_list if c not in punc]))

		# remove stopwords
		stop = set(stopwords.words('english'))
		words = [word for word in no_punc if word not in stop]

		# stem/lemmatize cleaned words
		lemmatizer = WordNetLemmatizer()
		return [lemmatizer.lemmatize(word) for word in words]

	def mine_topics(self, text, num_words=3, num_topics=3, passes=50):
		tokenized = [self.tokenize(sentence) for sentence in text]
		word_dict = self.dictionary(tokenized)
		term_matrix = [word_dict.doc2bow(word) for word in tokenized]
		ldamodel = self.lda(term_matrix, num_topics=num_topics, id2word=word_dict, passes=passes)
		return ldamodel.print_topics(num_topics=num_topics, num_words=num_words)

class SentimentAnalysis:
	def __init__(self):
		from nltk.sentiment.vader import SentimentIntensityAnalyzer
		self.sia = SentimentIntensityAnalyzer()

	def get_text_polarity(self, text):
		return self.sia.polarity_scores(text)

	def get_group_polarity(self, data):
		group = {}

		for kwd, descs in data.items():
			polarities = {src: self.get_text_polarity(str(desc)) for src, desc in descs}
			if polarities == {}:
				continue 

			sent_scores = [list(score.values()) for score in list(polarities.values())]
			agg_polarity = {'pos': 0.0, 'neu': 0.0, 'neg': 0.0, 'compound': 0.0}

			for sents in sent_scores:
				agg_polarity['pos'] += sents[0]
				agg_polarity['neu'] += sents[1]
				agg_polarity['neg'] += sents[2]
				agg_polarity['compound'] += sents[3]

			len_sent_scores = len(sent_scores)
			for key in agg_polarity.keys():
				agg_polarity[key] /= len_sent_scores

			polarities.update({'agg': agg_polarity})
			group.update({kwd: polarities})

		return group


# (TEST ANALYSIS.py)
"""
if __name__ == '__main__':

	doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
	doc2 = "My father spends a lot of time driving my sister around to dance practice."
	doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
	doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
	doc5 = "Health experts say that Sugar is not good for your lifestyle."
	doc_complete = [doc1, doc2, doc3, doc4, doc5]

	#ta = TopicAnalysis()
	#print(ta.mine_topics(doc_complete))

	import poller
	from constants import fin_sources
	p = poller.Poller('bac1eed426c8416992bad5823b10a779', [])
	data = p.get_articles(['AMD', 'trump'], fin_sources)

	sa = SentimentAnalysis()
	print(sa.get_group_polarity(data))
"""