import sentimine 
if __name__ == '__main__':

	## TEST GET SENTIMENT DICT ##
	s = sentimine.SentiMine('bac1eed426c8416992bad5823b10a779')
	print(s.get_sentiment_dict(['AMD', 'trump', 'fed', 'russia', 'market', 'congress']))

	## TEST GET TOPIC DICT ##