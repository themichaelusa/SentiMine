
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet
from itertools import chain

adjTags = ["JJ", "JJR", "JJS"]
nounTags = ["NN", "NNS", "NNP"]
verbTags = ["VBD", "VBG", "VBN", "VBP", "VBZ"]

def findSynonym(word):
	synonyms = wordnet.synsets(word)
	lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
	return list(lemmas)

class SentimentAnalysis:
	def __init__(self):
		self.words = {}
		self.availible_words = []
		self.trainingset = []
		self.createTrainingSet()
		self.classifer = nltk.NaiveBayesClassifier
		self.train()

	def tokenize_sentence(self, sentence): 
		words = sentence.split(" ")
		tokenized = {}
		for word in words:
			word_lc = word.lower()
			try:
				tokenized.update({word_lc: self.words[word_lc]})
			except KeyError as e:
				##TODO: key error exception --> look for synonyms (DONE)
				synons = findSynonym(word_lc)
				match = None
				for w in synons:
					if w in self.availible_words:
						match = w
						break
				if match is not None:
					tokenized.update({word_lc: self.words[match]})
		return tokenized

	def createTrainingSet(self):
		### populate words 
		def push_lexicon(name, label):
			pos_file = open(name, "r", encoding="ISO-8859-1") 
			idx = 0
			for line in pos_file: 
				if idx > 35: #line after lisense blurb + blank space
					line = line[:len(line)-1]
					if label == "pos":
						self.words.update({line: True})
					else:
						self.words.update({line: False})
				else:
					idx += 1 

		push_lexicon("lexicons/positive-words.txt", "pos")
		push_lexicon("lexicons/negative-words.txt", "neg")
		self.availible_words = self.words.keys()

		def tokenize_with_label(sentiment, label):
			out = None
			if label == "pos":
				return bool(sentiment)
			elif label == "neg":
				return bool(not sentiment)

		### load & tokenize pos/neg sentences 
		def load_training_data(name):
			file = open(name, "r", encoding="ISO-8859-1")

			for line in file:
				split_ln = line.split(" ")
				sent_score = split_ln[len(split_ln)-1]
				label = None
				if sent_score == 1: 
					label = "pos"
				else:
					label = "neg"

				token_wrt_label = tokenize_with_label
				tokenized_sentence = self.tokenize_sentence(line)
				tokened_and_labelled = {w:token_wrt_label(s, label) for w,s in tokenized_sentence.items()}

				if tokened_and_labelled != {}:
					self.trainingset.append((dict(tokened_and_labelled), label))

		load_training_data('sentences/yelp_labelled.txt')
		load_training_data('sentences/imdb_labelled.txt')
		load_training_data('sentences/amazon_cells_labelled.txt')

	def train(self):
		self.classifer.train(self.trainingset)

	def classify(self): 
		pass

def buildAnalysisProfile(text):

	from textblob import TextBlob
	analysis = TextBlob(text)
	analysisDict = {
	"Adj": [],
	"Noun": [],
	"Verb": [],
	"Adj-Noun": [],
	"Verb-Adj": [],
	"Noun-Phrases": [str(p) for p in list(analysis.noun_phrases)],
	"Sentences": [str(s) for s in list(analysis.sentences)]
	}

	tagsLen = len(analysis.tags)
	for idx, tagTup in enumerate(analysis.tags):
		tag = tagTup[1]
		
		# get Adj, Noun, Verbs separated 
		if tag in adjTags:
			analysisDict["Adj"].append(tagTup[0])
		elif tag in nounTags:
			analysisDict["Noun"].append(tagTup[0])
		elif tag in verbTags:
			analysisDict["Verb"].append(tagTup[0])

		#get Adj-Noun, Verb-Adj pairs going (if not out of bounds)
		if idx+1 < tagsLen:
			#adj-noun
			if analysis.tags[idx][1] in adjTags and analysis.tags[idx+1][1] in nounTags:
				analysisDict["Adj-Noun"].append(analysis.tags[idx][0] + " " + analysis.tags[idx+1][0])
			#verb-adj
			if analysis.tags[idx+1][1] in verbTags and analysis.tags[idx][1] in adjTags:
				analysisDict["Verb-Adj"].append(analysis.tags[idx][0] + " " + analysis.tags[idx+1][0])

def main(): pass

