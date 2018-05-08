from setuptools import setup

setup(
  name = 'sentimine',
  packages = ['sentimine'],
  version = '0.01',
  description = 'Get market sentiment on any keyword, instantly.',
  author = 'Michael Usachenko',
  author_email = 'meu2@illinois.edu',
  url = 'https://github.com/themichaelusa/SentiMine', 
  download_url = 'https://github.com/themichaelusa/SentiMine/archive/0.01.tar.gz', 
  install_requires=['nltk', 'requests'],
  keywords = ['SentiMine', 'sentiment', 'mining', 'topic', 'analysis', 'trading'],
  classifiers = [],
)