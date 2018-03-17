
"""

def test(reduced=False):
	tagged_sentences = []
	def load_sentences(name, list_ref):
		pos_file = open(name, "r", encoding="ISO-8859-1") 
		for line in pos_file:
			split_ln = line.split(" ")
			sent_score = split_ln[len(split_ln)-1]
			label = None
			if sent_score == 1: 
				label = "pos"
			else:
				label = "neg"
			list_ref.append((line, label))

	load_sentences('sentences/yelp_labelled.txt', tagged_sentences)
	load_sentences('sentences/imdb_labelled.txt', tagged_sentences)
	load_sentences('sentences/amazon_cells_labelled.txt', tagged_sentences)

	reduced_words = []
	if reduced:
		for sentence, sentiment in tagged_sentences:
			analysis = build_analysis_profile(sentence.lower())
			reduced_words.extend(analysis["Adj"]+analysis["Noun"]+analysis["Verb"])
	reduced_words = list(set(reduced_words))

	#print(reduced_words)
	#all_words = set(chain(*[word_tokenize(i[0].lower()) for i in tagged_sentences]))
	
	feature_set = []
	for sentence, sentiment in tagged_sentences:
		token = word_tokenize(sentence)
		#TODO: add synonym checking
		feature_set.append(({i:(i in token) for i in reduced_words}, sentiment))
	
	feature_set = []
	tokenize = word_tokenize
	for sentence, sentiment in tagged_sentences:
		token = {word.lower(): True for word in tokenize(sentence)}
		feature_set.append((token, sentiment))
		#feature_set.append(({i:(i in token) for i in reduced_words}, sentiment))

	return feature_set


training = test(reduced=True)
classifier = nltk.NaiveBayesClassifier
classifier.train(training)
print(training)
"""

"""
def clean_and_tokenize(sentence):
	#words = [word for word in sentence.split(" ") if not in stopset]
	tokenized = {}
	stemmer = PorterStemmer()
	for word in sentence.split(" "):
		lc_word = word.lower()
		if lc_word not in stopset:
			stemmed = stemmer.stem(lc_word)
			tokenized.update({stemmed: True})
			# stem words

	return tokenized

"""
"""
from nltk.corpus import stopwords
stopset = list(set(stopwords.words('english')))
from nltk.stem.porter import *
from textblob import TextBlob

def tag_string(string):
	tb = TextBlob(string)
	sentences = tb.sentences
	stemmer = PorterStemmer()

	for sentence in sentences:

		## stopword removal, porter stemming 
		cleaned_sentence = []
		for word in sentence.words:
			lc_word = word.lower()
			if lc_word not in stopset:
				stemmed = stemmer.stem(lc_word)
				cleaned_sentence.append(stemmed)

		concatenated = ' '.join(cleaned_sentence)
		#print(concatenated)
		words = TextBlob(concatenated)

		nt_sentiment = words.sentiment
		out = {
		"sentiment" : None,
		"polarity": nt_sentiment.polarity,
		"subjectivity": nt_sentiment.subjectivity
		}

		## classify as neg, pos, neu
		polarity = out['polarity']
		if polarity >= .1:
			out['sentiment'] = 'pos'
		elif polarity <= -.1:
			out['sentiment'] = 'neg'
		else:
			out['sentiment'] = 'neu'

tag_string(test_str)
"""
"""
for sentence, sentiment in tagged_sentences:
	words = TextBlob(sentence)
	nt_sentiment = words.sentiment
	out = {
	"sentiment" : None,
	"polarity": nt_sentiment.polarity,
	"subjectivity": nt_sentiment.subjectivity
	}

	## classify as neg, pos, neu
	polarity = out['polarity']
	if polarity >= .1:
		out['sentiment'] = 'pos'
	elif polarity <= -.1:
		out['sentiment'] = 'neg'
	else:
		out['sentiment'] = 'neu'

	print(out)

	#cleaned = clean_and_tokenize(sentence)
	#tokenized.append((cleaned, sentiment))

"""

"""
testStr = "Holy fuck, that was a terrible day."
from nltk.collocations import BigramCollocationFinder
bigram_finder = BigramCollocationFinder.from_words(testStr)
print(bigram_finder)

"""
"""
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
 
def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])
 
evaluate_classifier(bigram_word_feats)
"""

"""
class SentimentAnalysis:
	def __init__(self):
		self.words = {}
		self.availible_words = []
		self.trainingset = []
		self.classifer = nltk.NaiveBayesClassifier
		self.init_and_train_classifier()

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

	def init_and_train_classifier(self):
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
		self.classifer.train(self.trainingset)

	def classify(self, text, train=False): 
		#split_by_newline = text.split('\n')
				classify_results = []
		for line, pos in enumerate(split_by_newline):
			print(line)
			token = self.tokenize_sentence(line)
			classified = self.classifer.classify(token)
			classify_results.append((pos,classified))
		return classify_results
		token = self.tokenize_sentence(text)
		return self.classifer.classify(token, self.trainingset)
		#classify_results.append((pos,classified))

#sa = SentimentAnalysis()
#print(sa.classify("Hello, I'm Michael and it's great to meet you"))
"""
"""
def test_vader():
	training_data = subjectivity.sents(categories='subj')[:4750] + subjectivity.sents(categories='obj')[:4750]
	test_data = subjectivity.sents(categories='subj')[4750:4999] + subjectivity.sents(categories='obj')[4750:4999]

	sent_analyzer = SentimentAnalyzer()

	# mark negative/negation words 
	marked_neg_words = [mark_negation(sent) for sent in training_data]
	all_neg_words = sent_analyzer.all_words(marked_neg_words)

	# get unigram features WITH negation
	uni_feats = sent_analyzer.unigram_word_feats(all_neg_words, min_freq=20)
	sent_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=uni_feats)

	#apply features to tokenizd subj/obj lists s
	training_set = sent_analyzer.apply_features(training_data)
	test_set = sent_analyzer.apply_features(test_data)

	# train classifier 
	trainer = nltk.NaiveBayesClassifier.train
	classifier = sent_analyzer.train(trainer, training_set)

	#classifier accuracy 
	#print(sent_analyzer.evaluate(test_set[:50]).items())

	#test_txt = "Hey Now. The weather is sunny with a chance of a massive downpour!"
	#tokenize(test_txt)
	test_txt = "Most automated sentiment analysis tools are shit."
	print(classifier.classify(tokenize(test_txt)))
	
test_vader()
"""