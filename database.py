import sqlite3

with sqlite3.connect("Game.db") as db:
	cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
emailAddress VARCHAR(20) NOT NULL, 
password VARCHAR(20) NOT NULL,
login_count VARCHAR(10) NOT NULL DEFAULT '0',
account_type CHAR(1) NOT NULL DEFAULT '1',
sitestate CHAR(1) NOT NULL DEFAULT '0',
signup VARCHAR(255) NOT NULL DEFAULT '',
money VARCHAR(255) NOT NULL DEFAULT '1500'
level VARCHAR(255) NOT NULL DEFAULT '1',
exp INTEGER  NOT NULL DEFAULT 0,
rank VARCHAR(255) NOT NULL DEFAULT '0',
health CHAR(3) NOT NULL DEFAULT '100',
points VARCHAR(10) NOT NULL DEFAULT '0');
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS newspaper(                                          
sd INTEGER PRIMARY KEY, title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
r.execute("""
INSERT INTO users(username, emailAddress, password)
VALUES("test_user", "qasimimtiaz60@gmail.com", "545127")
""")

''')



cursor.execute("""
INSERT INTO users(username, emailAddress, password)
VALUES("test_user", "qasimimtiaz60@gmail.com", "545127")
""")

db.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

cursor.execute('''
CREATE TABLE IF NOT EXISTS replys (
	id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
	name VARCHAR(20) NOT NULL DEFAULT '',
	message TEXT NOT NULL, 
	tid INT(11) NOT NULL DEFAULT '',
	topictype char(1) NOT NULL DEFAULT 1);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sitestats (
	id INT(1) NOT NULL PRIMARY KEY AUTO_INCREMENT.
	admins TEXT NOT NULL, 
	mods TEXT NOT NULL, 
	mods_ip TEXT NOT NULL, 
	hdo TEXT NOT NULL, 
	ranks TEXT NOT NULL, 
	wealth TEXT NOT NULL, 
	cars TEXT NOT NULL);''')	
