import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response
import sqlite3
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)
app.secret_key = 'A0Zr98j /3 yX R~XHH!jmN]LWX / ,? RT'

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != '' and request.form['password'] != '':
			username = request.form['username'] 
			password_candidate = request.form['password']
			with sqlite3.connect("Game.db") as db:
				cursor = db.cursor()
			find_user = ("SELECT username, emailAddress, password FROM Users WHERE username=?")
			cursor.execute(find_user,[username])
			results = cursor.fetchall()
			
			if results:	
				for row in results:
					password = row[2]
					if sha256_crypt.verify(password_candidate,password):
						session['logged_in'] = True
						session['username'] = username
						return redirect(url_for('.dashboard'))
				msg = "Password is not correct!"
				return render_template('login.html',msg=msg)
			else:	
				msg = "Username is not correct!"
				return render_template('login.html',msg=msg)
		else:
			msg =  'One or more input boxes are empty' 
			return render_template('login.html',msg=msg)
	else:
		return render_template('login.html')

class RegisterForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),                                           
		validators.EqualTo('confirmed', message='Passwords do not match')	 
        ])
	confirmed = PasswordField('Confirm Password')			


def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('.login'))
	return wrap

@app.route('/missions')
@is_logged_in
def missions():
	return render_template('missions.html')


@app.route('/userList')
@is_logged_in
def userList():
	con = sqlite3.connect("Game.db")
	con.row_factory = sqlite3.Row
	cursor = con.cursor()
        cursor.execute("SELECT * FROM Users")
	users = cursor.fetchall()
	return render_template("users.html",users = users)

@app.route('/userList/<string:id>/')
@is_logged_in
def user(id):
	con = sqlite3.connect("Game.db")
	con.row_factory = sqlite3.Row
	cursor = con.cursor()
	cursor.execute("SELECT * FROM Users WHERE userId = ?", [id])
	user = cursor.fetchone()
	return render_template('user.html', user=user)
	
	
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	return redirect(url_for('login'))
	

@app.route('/dashboard')
@is_logged_in
def dashboard():
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	result = cursor.execute("SELECT * FROM HitmanNewspaper WHERE author = ?", [session['username']])
	articles = cursor.fetchall()
	if result > 0:
		cursor.execute("SELECT * FROM Users WHERE username = ?", [session['username']])
		user = cursor.fetchone()
		return render_template('dashboard.html', articles=articles, user=user)
	else:
		msg = 'No articles found'
		cursor.execute("SELECT * FROM Users WHERE username = ?", [session['username']])
                user = cursor.fetchone()
		return render_template('dashboard.html', msg=msg, user=user)
	cursor.close()

        
@app.route("/register/",methods=['POST', 'GET'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		emailAddress = form.email.data
		con = sqlite3.connect("Game.db") 
		cursor = con.cursor()
		cursor.execute("""SELECT * FROM Users WHERE username = ? OR emailAddress = ?""", (username, emailAddress))
		results = cursor.fetchall()
		if results:
			
			return "Username or email address already exists!"
		else:
			insertData = '''INSERT INTO Users(username,emailAddress,password)
                        VALUES(?,?,?)'''
                        cursor.execute(insertData, (username,emailAddress,password))
                        con.commit()
                        cursor.close()
                        flash('You are now registered and log in', 'success')
                        return redirect(url_for('.login'))
	else:
		return render_template("register.html", form=form)


@app.route('/KillPeasant')
@is_logged_in
def shootPeasant():
	
	result = ''				
	con = sqlite3.connect("Game.db") 
       	cursor=con.cursor()
	cursor.execute("SELECT * FROM Users WHERE username=?", [session['username']])
	results = cursor.fetchall()
	if results:
		for row in results:
			exp = row[10]
		for row in results:
			money = row[11]
		for row in results:
			brave = row[13]
		
		if brave >= 1:
			if exp >= 5:
			
				money += 100
				exp += 1
				brave = brave - 1
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
				cursor.execute("""UPDATE Users SET exp2 = ? WHERE username = ?""", (exp,session['username']))
				con.commit()
				cursor.execute("""UPDATE Users SET money2 = ? WHERE username=?""", (money, session['username']))
				con.commit()
	
				level = 0		
				if exp >= 100 and exp <= 200:
					level = 2
				elif exp >= 200 and exp <= 400:
					level = 3
				elif exp >= 400 and exp <= 800:
					level = 4
				elif exp >= 800 and exp <= 1600:
					level = 5
				elif exp >= 1600 and exp <= 3200:
					level = 6
				elif exp >= 3200 and exp <= 6400:
					level = 7
				elif exp >= 6400 and exp <= 12800:
					level = 8
				elif exp >= 12800 and exp <= 25600:
					level = 9
				elif exp >= 25600 and exp <= 51200:
					level = 10
				elif exp >= 51200 and exp <= 102400:
					level = 11
				elif exp >= 102400 and exp <= 204800:
					level = 12
				elif exp >= 204800 and exp <= 409600:
					level = 13
				elif exp >= 409600 and exp <= 819200:
					level = 14
				elif exp >= 1638400 and exp <= 3276800:
					level = 15
				else:
					for row in results:
                        			level = row[12]

			
							
				cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))
				con.commit()
				 
				msg = "You have been offered a contract by a unknown person who calls himself the Annoymous. He is offering $100 if you successfully kill a peasnt who has stole thousands dollars worth of gold from Annoymous.  You went to the nearby ghetto and successfully shot the peasant with a pistol and killed him! When Annoymous have heard about this great news, he have given you $100 in cash!"
				result = render_template("missionResponse.html", msg=msg)
				
			else:
				brave = brave - 1
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                con.commit()
				msg = " You have been offered a contract by a unknown person who calls himself the Annoymous. He is offering $100 if you successfully kill a peasnt who has stole thousands dollars worth of gold from Annoymous.  You went to the nearby ghetto, spotted the peasant, pulled the pistol trigger and shot the peasant with a pistol but have only managed to injure him a bit. The nearby gang heard you so you you have run for your life!"
				
				result = render_template("missionResponse.html", msg=msg)
		else:
			msg = "You do not have enough brave to attempt this mission!"
			result = render_template("missionResponse.html", msg=msg)
	else:
		result =  "Username not found!"
	return result 
 		
	
		
@app.route('/KillLoanShark')
@is_logged_in
def KillLoanShark():
	result = ''
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	cursor.execute("SELECT * FROM Users WHERE username=?", [session['username']])
	results = cursor.fetchall()
	if results:
		for row in results:
			exp = row[10]
		for row in results:
			money = row[11]
		for row in results:
			brave = row[13]
		if brave >= 2:
			if exp >= 100:
				money += 400
				exp += 10
				brave = brave - 2
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username = ?""", (brave, session['username']))
				cursor.execute(""" UPDATE Users SET exp2 = ? WHERE username = ?""", (exp, session['username']))
				cursor.execute(""" UPDATE Users SET money2 = ? WHERE username = ?""", (money, session['username']))
				con.commit()
				
				level = 0 
			
                                if exp >= 100 and exp <= 200:
                                        level = 2
                                elif exp >= 200 and exp <= 400:
                                        level = 3
                                elif exp >= 400 and exp <= 800:
                                        level = 4
                                elif exp >= 800 and exp <= 1600:
                                        level = 5
                                elif exp >= 1600 and exp <= 3200:
                                        level = 6
                                elif exp >= 3200 and exp <= 6400:
                                        level = 7
                                elif exp >= 6400 and exp <= 12800:
                                        level = 8
                                elif exp >= 12800 and exp <= 25600:
                                        level = 9
                                elif exp >= 25600 and exp <= 51200:
                                        level = 10
                                elif exp >= 51200 and exp <= 102400:
                                        level = 11
                                elif exp >= 102400 and exp <= 204800:
                                        level = 12
                                elif exp >= 204800 and exp <= 409600:
                                        level = 13
				elif exp >= 409600 and exp <= 819200:
                                        level = 14
                                elif exp >= 1638400 and exp <= 3276800:
                                        level = 15
                                else:
                                        for row in results:
                                                level = row[12] 
				cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))
                                con.commit()
				msg = "You have been hired to kill a loan shark by a unknown person that call himself annnoymous. You went to the loan shark tent and while he was making deals, you have shot him with a machine gun few times till he stop breathing and cut him in pieces. Took him back to Annoymous and recieved $400 in cash!"
				result = render_template('missionResponse.html', msg=msg)
			else:
				brave = brave - 2
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                con.commit()
				msg = "You have been hired to kill a loan shark by a unknown person that call himself annnoymous. You went to the loan shark tent and while he was making deals, you shot your machine gun and missed him. You then quickly left the premises before anyone saw you!"
				
			
				result = render_template('missionResponse.html', msg=msg)
		else:
			msg = "You do not have enough brave to attempt this mission!"
			result = render_template('missionResponse.html', msg=msg)
	else:
		return "Username not found"
	return result


@app.route('/KillBusinessMan')
@is_logged_in
def KillBusinessMan():
	result = ''
	con = sqlite3.connect("Game.db")
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", [session['username']])
        results = cursor.fetchall()
        if results:
                for row in results:
                        exp = row[10]
                for row in results:
                        money = row[11]
                for row in results:
                        brave = row[13]

                if brave >= 3:
                        if exp >= 1600:

                                money += 1600
                                exp += 100
                                brave = brave - 3
                                cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                cursor.execute("""UPDATE Users SET exp2 = ? WHERE username = ?""", (exp,session['username']))
                                con.commit()
                                cursor.execute("""UPDATE Users SET money2 = ? WHERE username=?""", (money, session['username']))
                                con.commit()

                                level = 0
                                if exp >= 100 and exp <= 200:
                                        level = 2
                                elif exp >= 200 and exp <= 400:
                                        level = 3
                                elif exp >= 400 and exp <= 800:
                                        level = 4
                                elif exp >= 800 and exp <= 1600:
                                        level = 5
                                elif exp >= 1600 and exp <= 3200:
                                        level = 6
                                elif exp >= 3200 and exp <= 6400:
                                        level = 7
                                elif exp >= 6400 and exp <= 12800:
                                        level = 8
                                elif exp >= 12800 and exp <= 25600:
                                        level = 9
                                elif exp >= 25600 and exp <= 51200:
                                        level = 10
                                elif exp >= 51200 and exp <= 102400:
                                        level = 11
                                elif exp >= 102400 and exp <= 204800:
                                        level = 12
                                elif exp >= 204800 and exp <= 409600:
                                        level = 13
				elif exp >= 409600 and exp <= 819200:
                                        level = 14
                                elif exp >= 1638400 and exp <= 3276800:
                                        level = 15
                                else:
                                        for row in results:
                                                level = row[12]
				cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))
                                con.commit()

                                msg = "You have been approached by a unknown person that call himself the Annoymous. He has hired you to kill a owner of a Tech Company that worth billions which have been giving away data about Annoymous and promised to give cash in return. You have went to this person mansions and  killed all of the security guards front of his mansion. You went inside the mansion and saw a man reading a weried but fascinating book in his study room. You have struck a big maschete on on his back and watched him bled to death. You went back to Annoymous and told him about the good news. Annoymous has rewarded you $1600 in cash. Congratulations!"
                                result = render_template("missionResponse.html", msg=msg)

                        else:
				brave = brave - 3
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
				con.commit()
                                msg = "You have been approached by a unknown person that call himself the Annoymous. He has hired you to kill a owner ofa Tech compani that worth billiions for giving away data about Annoymous and promised to give cash in return. You have went to this person  mansion but there was security guards outside his house and you do not have the capacity to kill them so you have left the premises!"
                                result = render_template("missionResponse.html", msg=msg)
                else:
                        msg = "You do not have enough brave to attempt this mission!"
                        result = render_template("missionResponse.html", msg=msg)
        else:
                result =  "Username not found!"
	return result 
@app.route('/KillLawyer')
@is_logged_in
def KillLawyer():
	result = ''
 	con = sqlite3.connect("Game.db")
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", [session['username']])
        results = cursor.fetchall()
        if results:
                for row in results:
                        exp = row[10]
                for row in results:
                        money = row[11]
                for row in results:
                        brave = row[13]

                if brave >= 4:
                        if exp >= 10000:

                                money += 6400
                                exp += 1000
                                brave = brave - 4
                                cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                cursor.execute("""UPDATE Users SET exp2 = ? WHERE username = ?""", (exp,session['username']))
                                con.commit()
                                cursor.execute("""UPDATE Users SET money2 = ? WHERE username=?""", (money, session['username']))
                                con.commit()

                                level = 0
                                if exp >= 100 and exp <= 200:
                                        level = 2
                                elif exp >= 200 and exp <= 400:
                                        level = 3
                                elif exp >= 400 and exp <= 800:
                                        level = 4
                                elif exp >= 800 and exp <= 1600:
                                        level = 5
                                elif exp >= 1600 and exp <= 3200:
                                        level = 6
                                elif exp >= 3200 and exp <= 6400:
                                        level = 7
                                elif exp >= 6400 and exp <= 12800:
                                        level = 8
                                elif exp >= 12800 and exp <= 25600:
                                        level = 9
                                elif exp >= 25600 and exp <= 51200:
                                        level = 10
				elif exp >= 51200 and exp <= 102400:
                                        level = 11
                                elif exp >= 102400 and exp <= 204800:
                                        level = 12
                                elif exp >= 204800 and exp <= 409600:
                                        level = 13
				elif exp >= 409600 and exp <= 819200:
                                        level = 14
                                elif exp >= 1638400 and exp <= 3276800:
                                        level = 15
                                else:
                                        for row in results:
                                                level = row[12]
                                cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))
                                con.commit()

                                msg = "You have been approached by a unknown person that call himself the Annoymous. He has offered you a contract to kill a well known lawyer  that has contributed to the life sentence of one of the Annoymous side men. If you succeed, you would be given $6400 in cash.  You have accepted this contract and off you went to the City Law Firm. You have asked the receptionist to book a appointment with this specific Lawyer. She booked you a appointment for next Friday. In the following friday, you have visited the City Law Firm to attend the appointment with the Lawyer. You have quickly took down the security cameras and took out your AK-47 and fired hundred of bullets towards the Lawyer and quickly left the premises. When Annoymous have heard about this great news, hhe has rewarded you $6400 in cash."
                                result = render_template("missionResponse.html", msg=msg)

                        else:
                                brave = brave - 4
                                cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                con.commit()
                                msg = " You have been approached by a uknown person that calls himself te Annoymous. He has offered you a contract to kill a well known Lawyer that has contributed to the life sentence of one of the Annoymous side man. If you succeed, you would be given $6400 in cash.  You have accepted this contract and off you went to the City Law Firm. You have asked the receptionist to book a appointment with this specific Lawyer. She booked you a appointment for next Friday. In the following friday, you have visited the City Law Firm to attend the appointment with the Lawyer. You have quickly took down the security cameras You have quickly took down the security cameras but before you took out your AK-47, the security guards have ambushed the door so you have quickly jumped out of the window."
                                result = render_template("missionResponse.html", msg=msg)
                else:
                        msg = "Youu do not have enough brave to attempt this mission!"
                        result = render_template("missionResponse.html", msg=msg)
        else:
                result =  "Username not found!"
        return result

@app.route('/KillPresident')
@is_logged_in
def KillPresident():
	result = ''
	con = sqlite3.connect("Game.db")
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", [session['username']])
        results = cursor.fetchall()
        if results:
                for row in results:
                        exp = row[10]
                for row in results:
                        money = row[11]
                for row in results:
                        brave = row[13]

                if brave >= 5:
                        if exp >= 100000:

                                money += 25600
                                exp += 10000
                                brave = brave - 5
                                cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                cursor.execute("""UPDATE Users SET exp2 = ? WHERE username = ?""", (exp,session['username']))
                                con.commit()
                                cursor.execute("""UPDATE Users SET money2 = ? WHERE username=?""", (money, session['username']))
                                con.commit()

                                level = 0
                                if exp >= 100 and exp <= 200:
                                        level = 2
                                elif exp >= 200 and exp <= 400:
                                        level = 3
                                elif exp >= 400 and exp <= 800:
                                        level = 4
                                elif exp >= 800 and exp <= 1600:
                                        level = 5
                                elif exp >= 1600 and exp <= 3200:
                                        level = 6
                                elif exp >= 3200 and exp <= 6400:
                                        level = 7
                                elif exp >= 6400 and exp <= 12800:
                                        level = 8
                                elif exp >= 12800 and exp <= 25600:
                                        level = 9
                                elif exp >= 25600 and exp <= 51200:
                                        level = 10
				elif exp >= 51200 and exp <= 102400:
                                        level = 11
                                elif exp >= 102400 and exp <= 204800:
                                        level = 12
                                elif exp >= 204800 and exp <= 409600:
                                        level = 13
				elif exp >= 409600 and exp <= 819200:
                                        level = 14
                                elif exp >= 1638400 and exp <= 3276800:
                                        level = 15
                                else:
                                        for row in results:
                                                level = row[12]
                                cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))
                                con.commit()
                                msg = "You have been approached by a unknown person that call himself the Annoymous. He has offered you a contract to kill the president of your country. He is offering you $25600 in cash if you accept and succeed this mission! You have accepted this contract and off to the president headquarters you go. You entered the president headquarters. You went upstairs till you have reached the roof of the headquarters. Placed a suitcase that has a time bomb inside on the floor and quickly left the premises. When the time bomb went off, everyone in the building have been blown up to pieces and killed including the president. When Annoymous have heard this fascinating news, he have rewarded you $25600 in cash. Congratulations!"
                                result = render_template("missionResponse.html", msg=msg)

                        else:
                                brave = brave - 5
                                cursor.execute(""" UPDATE Users SET brave = ? WHERE username= ?""", (brave, session['username']))
                                con.commit()
                                msg = "You have been approached by a unknown person that call himself the Annoymous. He has offered you a contract to kill the president of your country. He is offering you $25600 in cash if you accept and succeed this mission! You have accepted this contract and off to the president headquarters you go. You entered the president headquarters. You placed went upstairs till you have reached the roof of the headquarters. Suddenly the building alarm went off and you have quickly jumped off the roof and ran away before anyone can see you. You have failed this mission!"
                                result = render_template("missionResponse.html", msg=msg)
                else:
                        msg = "Youu do not have enough brave to attempt this mission!"
                        result = render_template("missionResponse.html", msg=msg)
        else:
                result =  "Username not found!"
        return result
@app.route('/PointsMarket', methods = ['GET', 'POST'])
@is_logged_in
def PointsMarket():
	if request.method == 'POST':
		points = request.form['points']
		con = sqlite3.connect("Game.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM Users WHERE username = ?", [session['username']])
		results = cursor.fetchall()
		totalMoney = 50 * int(points)
		if results:
			for row in results:
				money = row[11]
			for row in results:
				pointsSql = row[14]
			if totalMoney <= money:
				money = money - totalMoney 
				pointsSql += int(points)
				cursor.execute(""" UPDATE Users SET money2 = ? WHERE username = ?""", (money, session['username']))
				cursor.execute(""" UPDATE Users SET points = ? WHERE username = ?""", (pointsSql, session['username']))
				con.commit()
				msg = "You have brought " + points + " points."
				return render_template("pointsMarket.html", msg=msg)
			else:
				msg = "You do not have enough money to buy this amount of points"
				return render_template("pointsMarket.html",msg=msg)
		else:
			return "Username do not exist"

	else:
		return render_template("pointsMarket.html")

@app.route('/PointsExchange')
@is_logged_in
def PointsExchange():
	return render_template('pointsExchange.html')

@app.route('/BraveRefill')
@is_logged_in
def RefillBrave():
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	cursor.execute("SELECT * FROM Users WHERE username =?", [session['username']])
	results = cursor.fetchall()
	if results:
		for row in results:
			brave = row[13]
		for row in results:
			points = row[14]
		if brave < 10:
			if points >= 25:
				brave = 10
				points = points - 25
				cursor.execute(""" UPDATE Users SET brave = ? WHERE username = ?""", (brave, session['username']))
				cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
				con.commit()
				msg = "You have 100% brave"
				return render_template('pointsExchangeResponse.html', msg=msg)
			else:
				msg = "You do not have enough points!"
				return render_template('pointsExchangeResponse.html', msg=msg)
		else:
			
			msg = "You already have full brave!"
			return render_template('pointsExchangeResponse.html', msg=msg)
	else:
		return "Username not found"

@app.route('/EnergyRefill')
@is_logged_in
def RefillEnergy():
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username =?", [session['username']])
        results = cursor.fetchall()
        if results:
        	for row in results:
                        energy = row[20]
                        points = row[14]
                if energy < 100:
                        if points >= 25:
                                energy = 100
                                points = points - 25
                                cursor.execute(""" UPDATE Users SET Energy  = ? WHERE username = ?""", (energy, session['username']))
                                cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                con.commit()
                                msg = "You have 100% energy!"
                                return render_template('pointsExchangeResponse.html', msg=msg)
                        else:
                                msg = "You do not have enough points!"
                                return render_template('pointsExchangeResponse.html', msg=msg)
                else:

                        msg = "You already have full energy!"
                        return render_template('pointsExchangeResponse.html', msg=msg)
        else:
                return "Username not found"

@app.route('/HealthRefill')
@is_logged_in
def RefillHealth():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username =?", [session['username']])
        results = cursor.fetchall()
        if results:
                for row in results:
                        health = row[28]
                        points = row[14]
                if health < 100:
                        if points >= 25:
                                health = 100
                                points = points - 25
                                cursor.execute(""" UPDATE Users SET Health  = ? WHERE username = ?""", (health, session['username']))
                                cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                con.commit()
                                msg = "You have refilled your health, you now have 100% Health!"
                                return render_template('pointsExchangeResponse.html', msg=msg)
                        else:
                                msg = "You do not have enough points!"
                                return render_template('pointsExchangeResponse.html', msg=msg)
                else:

                        msg = "You already have full health!"
                        return render_template('pointsExchangeResponse.html', msg=msg)
        else:
                return "Username not found"	

@app.route('/HappinessRefill')
@is_logged_in
def RefillHappiness():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username =?", [session['username']])
        results = cursor.fetchall()
        if results:
                for row in results:
                        happiness = row[25]
                        points = row[14]
			house = row[26]
		if house == "Streets":
		
                	if happiness < 100:
                        	if points >= 25:
                                	happiness = 100
                                	points = points - 25
                                	cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                	cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                	con.commit()
                                	msg = "You have 100% Happiness"
                               		return render_template('pointsExchangeResponse.html', msg=msg)
                        	else:
                                	msg = "You do not have enough points!"
                                	return render_template('pointsExchangeResponse.html', msg=msg)
			
                	else:

                        	msg = "You already have full happiness!"
                        	return render_template('pointsExchangeResponse.html', msg=msg)
		elif house == "Flat":
			if happiness < 200:
				if points >= 25:
					happiness = 200
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
			else:
				msg = "You already have full happiness!"
				return render_template('pointsExchangeResponse.html',msg=msg)
		
		elif house == "Terraced House":
			
			if happiness < 300:
                        	if points >= 25:
                                        happiness = 300
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
                        else:
                                msg = "You already have full happiness!"
                                return render_template('pointsExchangeResponse.html',msg=msg)
		
		elif house == "End of Terrace House":
			 if happiness < 400:
                                if points >= 25:
                                        happiness = 400
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                       	 	else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
					
                	 else:
                         	msg = "You already have full happiness!"
                         	return render_template('pointsExchangeResponse.html',msg=msg)
		elif house == "Semi Detached House":
			 if happiness < 500:
                                if points >= 25:
                                        happiness = 500
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
                         else:
                         	msg = "You already have full happiness!"
                         	return render_template('pointsExchangeResponse.html',msg=msg)

		elif house == "Detached House":
			 if happiness < 600:
                                if points >= 25:
                                        happiness = 600
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html', msg=msg)

                         else:
                         	msg = "You already have full happiness!"
                         	return render_template('pointsExchangeResponse.html',msg=msg)
		
		elif house == "Mansion":
			 if happiness < 700:
                                if points >= 25:
                                        happiness = 700
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html', msg=msg)
                         else:
                         	msg = "You already have full happiness!"
                         	return render_template('pointsExchangeResponse.html',msg=msg)
		
		elif house == "Castle":
			 if happiness < 800:
                                if points >= 25:
                                        happiness = 800
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
                         else:
                                msg = "You already have full happiness!"
                                return render_template('pointsExchangeResponse.html',msg=msg)
		
		elif house == "Palace":
			 if happiness < 900:
                                if points >= 25:
                                        happiness = 900
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
                         else:
                                msg = "You already have full happiness!"
                
		                return render_template('pointsExchangeResponse.html',msg=msg)
		elif house == "Private Island":
	
	      
			if happiness < 1000:
                                if points >= 25:
                                        happiness = 1000
                                        points = points - 25
                                        cursor.execute(""" UPDATE Users SET Happiness = ? WHERE username = ?""", (happiness, session['username']))
                                        cursor.execute(""" UPDATE Users SET points = ? WHERE points = ?""", (points, session['username']))
                                        con.commit()
                                        msg = "You have 100% Happiness"
                                        return render_template('pointsExchangeResponse.html', msg=msg)
                                else:
                                        msg = "You do not have enough points!"
					return render_template('pointsExchangeResponse.html',msg=msg)
                        else:
                                msg = "You already have full happiness!"
                                return render_template('pointsExchangeResponse.html',msg=msg)
		else:
			msg = "You have no house"
			return render_template('pointsExchangeResponse.html',msg=msg)

        else:
                return "Username not found"

@app.route('/newspaper')
@is_logged_in
def newspaper():
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	results = cursor.execute("SELECT * FROM HitmanNewspaper")
	articles  =  cursor.fetchall()
	if results > 0:
		return render_template('newspaper.html', articles=articles)
	else:
		msg = "No Articles Found"
		return render_template('newspaper.html',msg=msg)
	cursor.close()

@app.route('/newspaper/<string:id>/')
@is_logged_in
def article(id):
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	cursor.execute("SELECT * FROM HitmanNewspaper WHERE id = ?", [id])
	article = cursor.fetchone()
	return render_template('article.html', article=article)

class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
		con = sqlite3.connect("Game.db")
		cursor = con.cursor()
		cursor.execute("""INSERT INTO HitmanNewspaper(title, body, author) VALUES(?, ?, ?)""",(title, body, session['username']))
		con.commit()
		cursor.close()
		flash('Article Created', 'success')
		return redirect(url_for('dashboard'))
	
	return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	result = cursor.execute("SELECT * FROM HitmanNewspaper WHERE id =? AND author =?",(id, session['username']))
	article = cursor.fetchone()
	cursor.close()
	form = ArticleForm(request.form)
	form.title.data = article[1]
	form.body.data = article[3]
	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
		cursor = con.cursor()
		app.logger.info(title)
		cursor.execute("UPDATE HitmanNewspaper SET title=?, body=? WHERE id=?",(title, body, id))
		con.commit()
		cursor.close()
		return redirect(url_for('dashboard'))
	return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	cursor.execute("DELETE FROM HitmanNewspaper WHERE id = ?", [id])
	con.commit()
	cursor.close()
	flash('Article Deleted', 'success')
	return redirect(url_for('dashboard'))

@app.route('/uploadImage', methods = ['GET', 'POST'])
@is_logged_in
def uploadImage():
	
	if request.method == 'POST':
		try:				
			file = request.files['image']
			con = sqlite3.connect("Game.db")
			cursor = con.cursor()
			cursor.execute("SELECT * FROM Users WHERE username = ?",[session['username']])
			results = cursor.fetchall()
			if results:
				file.save('static/' + str(file.filename))
				cursor.execute("UPDATE Users SET DP = ? WHERE username = ?", (str(file.filename),session['username']))
				con.commit()
				msg = "You have successfully uploaded your profile picture"
				cursor.close()
				return render_template("uploadImage.html",msg=msg)
			else:
				return redirect(url_for("login.html"))
		except Exception as e:
			msg = "You have not uploaded a image!"
			return render_template("uploadImage.html", msg=msg)		
	else:	
		return render_template("uploadImage.html")
@app.route("/gym", methods = ['GET', 'POST'])
@is_logged_in
def gym():
	if request.method == 'POST':
		strength_gain = ''
		speed_gain = ''
		defence_gain = ''
		total_gain_string = ''
		if request.form['strength']:
			try:
				Energy_Used = float(request.form['strength'])
			
				con = sqlite3.connect("Game.db")
				cursor = con.cursor()
				cursor.execute("SELECT * FROM Users WHERE username = ?",[session["username"]])
				results = cursor.fetchall()
				if results:
					for row in results: 
						strength = row[21]
					for row in results:
						total_stats = row[24]
					for row in results:
						energy = row[20]
					for row in results:
						happiness = row[25]
					if Energy_Used <= energy:
						if energy > 0:
							total_gain =(((Energy_Used)/10) * (happiness/10))
							strength += total_gain
							total_stats += total_gain
							
							energy = energy - Energy_Used
							happiness = happiness - (Energy_Used/10)
						
							cursor.execute("UPDATE Users SET Strength = ? WHERE username = ?",(strength, session["username"]))
							cursor.execute("UPDATE Users SET Total_Stats = ? WHERE username = ?", (total_stats, session["username"]))
							cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?", (energy, session["username"]))
							cursor.execute("UPDATE Users SET Happiness = ? WHERE username = ?", (happiness, session["username"]))
							con.commit()
							msg = "You have trained " + str(Energy_Used) + " times and gained " + str(total_gain) + " strength and " + " now have " + str(strength) + " strength and " + str(total_stats) + " total stats."
							return render_template("gym.html", msg=msg)
						else:
							msg = "You do not have enough energy to train your stats!"
							return render_template("gym.html", msg=msg)
					else:
						msg = "You do not have that much energy to train that amount of times!"
						return render_template("gym.html", msg=msg)
				else:
					return "Username not found"
			except ValueError:
				msg = "Invalid input!"
				return render_template("gym.html",msg=msg)
		elif request.form['speed']:
                	try:
                        	Energy_Used = float(request.form['speed'])

                                con = sqlite3.connect("Game.db")
                                cursor = con.cursor()
                                cursor.execute("SELECT * FROM Users WHERE username = ?",[session["username"]])
                                results = cursor.fetchall()
                                if results:
                                        for row in results:
                                                speed = row[22]
                                        for row in results:
                                                total_stats = row[24]
                                        for row in results:
                                                energy = row[20]
                                        for row in results:
                                                happiness = row[25]
                                        if Energy_Used <= energy:
                                                if energy > 0:
                                                        total_gain =(((Energy_Used)/10) * (happiness/10))
                                                        speed += total_gain
                                                        total_stats += total_gain

                                                        energy = energy - Energy_Used
                                                        happiness = happiness - (Energy_Used/10)

                                                        cursor.execute("UPDATE Users SET Speed = ? WHERE username = ?",(speed, session["username"]))
                                                        cursor.execute("UPDATE Users SET Total_Stats = ? WHERE username = ?", (total_stats, session["username"]))
                                                        cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?", (energy, session["username"]))
                                                        cursor.execute("UPDATE Users SET Happiness = ? WHERE username = ?", (happiness, session["username"]))
                                                        con.commit()
                                                        msg = "You have trained " + str(Energy_Used) + " times and gained " + str(total_gain) + " speed and " + " now have " + str(speed) + " speed  and " + str(total_stats) + " total stats."
                                                        return render_template("gym.html", msg=msg)
                                                else:
                                                        msg = "You do not have enough energy to train your stats!"
                                                        return render_template("gym.html", msg=msg)
                                        else:
                                                msg = "You do not have that much energy to train that amount of times!"
                                                return render_template("gym.html", msg=msg)
                                else:
                                        return "Username not found"
			except ValueError:
                        	msg = "Invalid input!"
                                return render_template("gym.html",msg=msg)
		elif request.form['defence']:
               		try:
                        	Energy_Used = float(request.form['defence'])

                                con = sqlite3.connect("Game.db")
                                cursor = con.cursor()
                                cursor.execute("SELECT * FROM Users WHERE username = ?",[session["username"]])
                                results = cursor.fetchall()
                                if results:
                                        for row in results:
                                                defence = row[23]
                                        for row in results:
                                                total_stats = row[24]
                                        for row in results:
                                                energy = row[20]
                                        for row in results:
                                                happiness = row[25]
                                        if Energy_Used <= energy:
                                                if energy > 0:
                                                        total_gain =(((Energy_Used)/10) * (happiness/10))
                                                        defence += total_gain
                                                        total_stats += total_gain

                                                        energy = energy - Energy_Used
                                                        happiness = happiness - (Energy_Used/10)

                                                        cursor.execute("UPDATE Users SET Defence = ? WHERE username = ?",(defence, session["username"]))
                                                        cursor.execute("UPDATE Users SET Total_Stats = ? WHERE username = ?", (total_stats, session["username"]))
                                                        cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?", (energy, session["username"]))
                                                        cursor.execute("UPDATE Users SET Happiness = ? WHERE username = ?", (happiness, session["username"]))
                                                        con.commit()
                                                        msg = "You have trained " + str(Energy_Used) + " times and gained " + str(total_gain) + " defence and " + " now have " + str(defence) + " defence and " + str(total_stats) + " total stats."
                                                        return render_template("gym.html", msg=msg)
                                                else:
                                                        msg = "You do not have enough energy to train your stats!"
                                                        return render_template("gym.html", msg=msg)
                                        else:
                                                msg = "You do not have that much energy to train that amount of times!"
                                                return render_template("gym.html", msg=msg)
                                else:
                                        return "Username not found"
			except ValueError:
                        	msg = "Invalid input!"
                        	return render_template("gym.html",msg=msg)
		else:
			msg = "You have not entered anything in one of the input boxes"
			return render_template("gym.html",msg=msg)                                                                            
	else:
		return render_template("gym.html")

@app.route("/Real_Estate")
@is_logged_in
def real_estate():
	return render_template("real_estate.html")
@app.route("/Real_Estate/Flat")
@is_logged_in
def buy_flat():
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
	results = cursor.fetchall()
	if results:
		for row in results:
			money = row[11]
			happiness = row[25]
			house = row[26]
		if money >= 25000:
			if house != "Flat":
				money = money - 25000
				happiness = 200
				house = "Flat"
				cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username'])) 
				cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
				cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
				con.commit()
				msg = "You have sucessfully brought a flat!"
				return render_template("real_estate_response.html", msg=msg)
			else:
				msg = "You are already living in a Flat!"
				return render_template("real_estate_response.html", msg=msg)
		else:
			msg = "You do not have enough money to buy a Flat!"
			return render_template("real_estate_response.html", msg=msg)
@app.route("/Real_Estate/TerracedHouse")
@is_logged_in
def buy_terraced_house():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 50000:
                        if house != "Terraced House":
                                money = money - 50000
                                happiness = 300
                                house = "Terraced House"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Terraced House!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Terraced House!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Terraced House!"
                        return render_template("real_estate_response.html", msg=msg)
@app.route("/Real_Estate/EndOfTerrace")
@is_logged_in
def buy_end_of_terraced_house():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 100000:
                        if house != "End of Terrace House":
                                money = money - 100000
                                happiness = 400
                                house = "End of Terrace House"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a End of Terrace House!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a End of Terrace House!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a End of Terrace House!"
                        return render_template("real_estate_response.html", msg=msg)

@app.route("/Real_Estate/Semi_Detached_House")
@is_logged_in
def buy_semi_detached_house():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
        	for row in results:
                	money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 250000:
                	if house != "Semi Detached House":
                       		money = money - 250000
                                happiness = 500
                                house = "Semi-Detached House"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Semi Detached Houe!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Semi Detached House!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a semi detached house!"
                        return render_template("real_estate_response.html", msg=msg)	

@app.route("/Real_Estate/Detached_House")
@is_logged_in
def buy_detached_houe():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
        	for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 500000:
                        if house != "Detached House":
                                money = money - 500000
                                happiness = 600
                                house = "Detached House"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Detached House!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Detached House!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Detached House!"
                        return render_template("real_estate_response.html", msg=msg)		

@app.route('/Real_Estate/Mansion')
@is_logged_in
def buy_mansion():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 1000000:
                        if house != "Mansion":
                                money = money - 1000000
                                happiness = 700
                                house = "Mansion"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Mansion!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Mansion!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Mansion!"
                        return render_template("real_estate_response.html", msg=msg)

@app.route('/Real_Estate/Palace')
@is_logged_in
def buy_palace():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 25000000:
                        if house != "Palace":
                                money = money - 25000000
                                happiness = 900
                                house = "Palace"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Palace!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Palace!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Palace!"
                        return render_template("real_estate_response.html", msg=msg)
@app.route('/Real_Estate/Castle')
def buy_castle():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 5000000:
                        if house != "Castle":
                                money = money - 5000000
                                happiness = 800
                                house = "Castle"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Castle!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Castle!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Castle!"
                        return render_template("real_estate_response.html", msg=msg)
@app.route("/Real_Estate/Private_Island")
def buy_private_island():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [session["username"]])
        results = cursor.fetchall()
        if results:
                for row in results:
                        money = row[11]
                        happiness = row[25]
                        house = row[26]
                if money >= 100000000:
                        if house != "Private Island":
                                money = money - 100000000
                                happiness = 1000
                                house = "Private Island"
                                cursor.execute("UPDATE Users SET house = ? WHERE username = ?", (house, session['username']))
                                cursor.execute("UPDATE Users SET happiness = ? WHERE username = ?", (happiness, session['username']))
                                cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (money, session['username']))
                                con.commit()
                                msg = "You have sucessfully brought a Private Island!"
                                return render_template("real_estate_response.html", msg=msg)
                        else:
                                msg = "You are already living in a Private Island!"
                                return render_template("real_estate_response.html", msg=msg)
                else:
                        msg = "You do not have enough money to buy a Private Island!"
                        return render_template("real_estate_response.html", msg=msg)


@app.route('/send_message/<recipient>', methods = ['GET', 'POST'])
@is_logged_in
def send_message(recipient):
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
	
	form = ArticleForm(request.form)
        if request.method == 'POST' and form.validate():
		if recipient != session['username']:
          		subject  = form.title.data
              	 	message = form.body.data
                	cursor.execute("""INSERT INTO sent_messages(message, subject, username, username2) VALUES(?, ?, ?,?)""",(message, subject, recipient,session['username'] ))
			cursor.execute("""INSERT INTO recieved_messages(message,subject,username, username2) VALUES(?,?,?,?)""",(message, subject, session['username'], recipient))
			con.commit()
        	        cursor.close()
              	 	msg = "Message Sent"
               	 	return render_template('send_message.html',msg=msg,form=form)
		else:
			msg = "You can't send a message to yourself!"
			return render_template("send_message.html",msg=msg,form=form)

        return render_template('send_message.html', form=form, recipient=recipient)
@app.route('/view_message/<string:id>/')
@is_logged_in
def view_message(id):
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM recieved_messages WHERE message_id = ?", [id])
        mail = cursor.fetchone()
        return render_template('message.html', mail=mail)

@app.route('/view_sent_message/<string:id>/')
@is_logged_in
def view_sent_message(id):
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM recieved_messages WHERE message_id = ?", [id])
        mail = cursor.fetchone()
        return render_template('sent_message.html', mail=mail)
	
@app.route('/mailbox')
@is_logged_in
def mailbox():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        results = cursor.execute("SELECT * FROM recieved_messages WHERE username2 = ?", [session['username']])
        mails  =  cursor.fetchall()
        if results > 0:
                return render_template('mailbox.html', mails=mails)
        else:
                msg = "No messages"
                return render_template('mailbox.html', mails=mails)
        cursor.close()	

@app.route('/Sent_Messages')
@is_logged_in
def sent_messages():
	con = sqlite3.connect("Game.db")
        cursor = con.cursor()
        results = cursor.execute("SELECT * FROM sent_messages WHERE username2 = ?", [session['username']])
        mails  =  cursor.fetchall()
        if results > 0:
                return render_template('outbox.html', mails=mails)
        else:
                msg = "No messages"
                return render_template('outbox.html', mails=mails)
        cursor.close()

@app.route('/attack/<string:user>')
@is_logged_in
def attack_user(user):
	con = sqlite3.connect("Game.db")
	cursor = con.cursor()
      	cursor.execute("SELECT * FROM Users WHERE username=?",[session['username']])
	results = cursor.fetchall()
	total_stats1 = 0
	if results:
		if user != session['username']:
			cursor.execute("SELECT * FROM Users WHERE username=?",[user])
			results2 = cursor.fetchall()
		
			for row in results:
				exp = row[10]
				level = row[12]
				money = row[11]
				health = row[28]
				attacks = row[30]		
				total_stats = row[24]
				energy = row[20]		
			if results2:
				for row in results2:
					exp2 = row[10]
					level2 = row[12]
					money2 = row[11]
					health2 = row[28]
					attacks2 = row[30]
					strength2 = row[21]
					speed2 = row[22]
					defence2 = row[23]
					total_stats2 = row[24]
					energy2 = row[20]
				
				if energy >= 25:
					if health > 0:
						if health2 > 0:
							if total_stats > total_stats2:
								health2 = health2 - health2
								exp += exp2/10
								money +=  money2
								money3 = money2
								energy = energy - 25
								money2 = 0
								attacks = attacks + 1
								cursor.execute("UPDATE Users SET exp2 = ? WHERE username = ?",(exp,session["username"]))
								cursor.execute("UPDATE Users SET money2 = ? WHERE username = ?", (money, session["username"]))
								cursor.execute("UPDATE Users SET Health = ? WHERE username = ?", (health2, user))
								cursor.execute("UPDATE Users SET money2 = ? WHERE username = ?", (money2, user))
								cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?",(energy, session["username"]))
								cursor.execute("UPDATE Users SET attacks2 = ? WHERE username = ?", (attacks, session["username"]))
								level = 0
                        			      	  	if exp >= 100 and exp <= 200:
                                       					level = 2
                               					elif exp >= 200 and exp <= 400:
                                       					level = 3
                                				elif exp >= 400 and exp <= 800:
                                        				level = 4
                                				elif exp >= 800 and exp <= 1600:
                                        				level = 5
                                				elif exp >= 1600 and exp <= 3200:
                                        				level = 6
                                				elif exp >= 3200 and exp <= 6400:
                                        				level = 7
                                				elif exp >= 6400 and exp <= 12800:
                                        				level = 8
                                				elif exp >= 12800 and exp <= 25600:
                                       					level = 9
                                				elif exp >= 25600 and exp <= 51200:
                                        				level = 10
                                				elif exp >= 51200 and exp <= 102400:
                                        				level = 11
                                				elif exp >= 102400 and exp <= 204800:
                                        				level = 12
                                				elif exp >= 204800 and exp <= 409600:
                                        				level = 13
                                				elif exp >= 409600 and exp <= 819200:
                                        				level = 14
                                				elif exp >= 1638400 and exp <= 3276800:
                                        				level = 15
                               					else:
                                        				for row in results:
                                                				level = row[12]

                                				cursor.execute(""" UPDATE Users SET level3 = ? WHERE username = ?""", (level, session['username']))

								con.commit()
								msg = "You have attempted to attack " + user + " with a bakooza and blown up " + user + " brains out!" + " You have gained " + str(money3) + " in cash and " + str(exp2/10) + " in experience."
								return render_template('attack_response.html',msg=msg)
							elif total_stats < total_stats2:
								health = health - health 
								energy = energy - 25
								attacks = attacks + 1
								cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?", (energy,session["username"]))
								cursor.execute("UPDATE Users SET Health = ? WHERE username = ?",(health, session["username"]))
								cursor.execute("UPDATE Users SET attacks2 = ? WHERE username = ?", (attacks, session["username"]))
								con.commit()
								msg = "You have attempted to attack " + user + " with a bakooza but " + user + " fought back " + " and blown up you up with a Tank!"
								return render_template('attack_response.html', msg=msg)
						


							else:
								health = health - ((health)/2)
								health2 = health2 - ((health2)/2)
								attacks = attacks + 1
								energy = energy - 25
								cursor.execute("UPDATE Users SET Energy = ? WHERE username = ?", (energy,session["username"]))
                                              	 		cursor.execute("UPDATE Users SET Health = ? WHERE username = ?",(health, session["username"]))
                                               	 		cursor.execute("UPDATE Users SET attacks2 = ? WHERE username = ?", (attacks, session["username"]))
								cursor.execute("UPDATE Users SET Health = ? WHERE username = ?", (health2, user))
								msg = "You have attempted to attack " + user + " with a bazooka but " + user + " fought back " + " and then you fought back with a diamond knife and then " + user + " fought back with a AK47 " + "before you grabbed a hand grenade from your pocket, you have have heard sirens coming from a nearby place so you quickly left the area!"
						
								return render_template("attack_response.html",msg=msg)
					
						else:
							msg = "This person is currently unconscious!"
							return render_template("attack_response.html",msg=msg)
					else:

						msg = "You do not have enough health to attack this person!"
						return render_template("attack_response.html",msg=msg)
				else:
					msg = "You do not have enough energy to attack this person!"
					return render_template("attack_response.html", msg=msg)
			else:
				return "Username 2 not found!"
			
		else:
			msg = "Only a mental person would attack himself!"
                        return render_template("attack_response.html", msg=msg)


	else:
		return "Username 1 not found!"
	
	
	
@app.route('/')
def index():
	return render_template('home.html')

@app.route('/About')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)

