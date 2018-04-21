from constants import ALL_GOOD, EXISTING_KWD_ERROR

class DB:
	def __init__(self, dbname, user, pwd):
		import psycopg2
		conn = psycopg2.connect(dbname=dbname, user=user, password=pwd)
		self.cur = conn.cursor()

	def add_keyword(self, keyword): 
		table_names = self.cur.execute('SELECT * FROM information_schema.tables;')
		if keyword in table_names:
			return EXISTING_KWD_ERROR

		t_name = 'CREATE TABLE {}'.format(keyword)
		query = t_name + '(id timestamp, pos FLOAT, neu FLOAT, neg FLOAT, com FLOAT);'
		self.cur.execute(query)

	def write_to_keyword(self, sentiment): 
		pos, neu, neg, com = sentiment

	def get_keyword(self): pass

	def get_keyword_hist(self): pass







		
				