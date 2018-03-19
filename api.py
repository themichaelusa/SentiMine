from flask_api import FlaskAPI
from flask import request

app = FlaskAPI(__name__)	

@app.route('/addKeyword/<str:key>', methods=['PUT', 'POST'])
def add_keyword(key):
	if request.method == 'PUT' or  request.method == 'POST':
		## PUSH TO DB ##

@app.route('/getSentiment/<str:key>', methods=['GET', 'PUT', 'POST'])
def get_sentiment(key):
	if request.method == 'PUT' or  request.method == 'POST':
		## PUSH TO DB ##
	elif request.method == 'GET':
		## PULL FROM DB ##

@app.route('/getTopics/<str:key>', methods=['GET', 'PUT', 'POST'])
def get_topics(key):
	if request.method == 'PUT' or  request.method == 'POST':
		## PUSH TO DB ##
	elif request.method == 'GET':
		## PULL FROM DB ##

if __name__ == '__main__':
	app.run(debug=True)



		