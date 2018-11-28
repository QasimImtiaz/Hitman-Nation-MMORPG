import sqlite3
from flask import session

con = sqlite3.connect("Game.db")
cursor = con.cursor()
cursor.execute("SELECT * FROM Users WHERE username=?",[session['username']])
results = cursor.fetchall()
if results:
	for row in results:
		brave = row[13]
	brave += 1
	cursor.execute('''UPDATE Users SET brave = ? WHERE username = ?''',(brave, session['username']))
	con.commit()
else:
	print "Error"

