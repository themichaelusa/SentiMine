import poller
from constants import fin_sources

if __name__ == '__main__':
	p = poller.Poller('blah', [])
	print(p.get_articles(['AMD', 'trump'], fin_sources))

