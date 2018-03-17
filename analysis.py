
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
		no_punc = []
		all_chars = [list(word) for word in words]
		for char_list in all_chars:
			no_punc.append("".join([c for c in char_list if c not in punc]))

		# remove stopwords
		stop = set(stopwords.words('english'))
		words = [word for word in no_punc if word not in stop]

		# stem/lemmatize cleaned words
		lemmatizer = WordNetLemmatizer()
		return [lemmatizer.lemmatize(word) for word in words]

	def mine_topics(text, num_words=3, num_topics=3, passes=50):
		tokenized = self.tokenize(text)
		word_dict = self.dictionary(tokenized)
		term_matrix = [word_dict.word2bow(word) for word in tokenized]
		ldamodel = self.lda(term_matrix, num_topics=num_topics, id2word=dictionary, passes=passess)
		return ldamodel.print_topics(num_topics=num_topics, num_words=num_words)

class SentimentAnalysis:
	def __init__(self):
		from nltk.sentiment.vader import SentimentIntensityAnalyzer
		self.sia = SentimentIntensityAnalyzer()

	def get_text_polarity(text):
		tokenized = tokenize.sent_tokenize(text)
		return self.sia.polarity_scores(tokenized)


		



