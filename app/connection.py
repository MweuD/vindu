import MySQLdb

def connection():
	conn= MySQLdb.connect(host='localhost',
						  user='root',
						  passwd='Awesome95',
						  db='a_database')
	c = conn.cursor()
	return c, conn