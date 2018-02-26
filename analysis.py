
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
		self.trainingset = []
		self.createTrainingSet()
		self.

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

				token = {}
				for word in split_ln:
					##TODO: key error exception --> look for synonyms
					try:
						sentiment = self.words[word]
						out = None
						if label == "pos":
							out = {word: bool(sentiment)}
						elif label == "neg":
							out = {word: bool(not sentiment)}
						token.update(out)
					except KeyError as e:
						synons = findSynonym(word)
						match = None
						allkeys = self.words.keys()
						for w in synons:
							if w in allkeys:
								match = w
								break
						if match is not None:
							sentiment_match = self.words[match]
							out_match = None
							if label == "pos":
								out_match = {match: bool(sentiment_match)}
							elif label == "neg":
								out_match = {match: bool(not sentiment_match)}
							token.update(out_match)

				if token != {}:
					self.trainingset.append((token, label))

		load_training_data('sentences/yelp_labelled.txt')
		load_training_data('sentences/imdb_labelled.txt')
		load_training_data('sentences/amazon_cells_labelled.txt')

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



