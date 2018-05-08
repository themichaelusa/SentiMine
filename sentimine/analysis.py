
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

def find_synonym(word):
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

	def mine_topics(self, text, num_words=10, num_topics=5, passes=100):
		tokenized = [self.tokenize(sentence) for sentence in text]
		word_dict = self.dictionary(tokenized)
		term_matrix = [word_dict.doc2bow(word) for word in tokenized]
		ldamodel = self.lda(term_matrix, num_topics=num_topics, id2word=word_dict, passes=passes)
		return ldamodel.print_topics(num_topics=num_topics, num_words=num_words)

	def group_mine_topics(self, data):
		group = {}
		for kwd, descs in data.items():
			if descs == []:
				continue
			kwd_descs = [desc for src, desc in descs]
			all_desc = " ".join(kwd_descs)
			topics = self.mine_topics([all_desc])
			group.update({kwd: topics})
		return group

class SentimentAnalysis:
	def __init__(self):
		from nltk.sentiment.vader import SentimentIntensityAnalyzer
		self.sia = SentimentIntensityAnalyzer()

	def __get_text_polarity(self, text):
		return self.sia.polarity_scores(text)

	def get_group_polarity(self, data):
		group = {}
		for kwd, descs in data.items():
			polarities = {src: self.__get_text_polarity(str(desc)) for src, desc in descs.items()}
			if polarities == {}:
				group.update({kwd: polarities})
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
