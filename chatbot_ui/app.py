import os
import sys
import pylab
import wave
from datetime import date
from datetime import timedelta
from flask import Flask, render_template, request,jsonify,json,session,flash, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import hashlib
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from train import train_the_bot #separate function for training the bot
from convert_to_audio import convert_aud
from con_specto import convert_to_spectogram
from converter import Converter
from vid_avi import convert_to_avi
from connect_of import get_gaze_au_data
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
from queue import Queue 
from stat import S_ISREG, ST_CTIME, ST_MODE
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector



md5_audio=0
md5_video=0
#chatbot = ChatBot("da",storage_adapter='chatterbot.storage.SQLStorageAdapter',filters=["chatterbot.filters.RepetitiveResponseFilter"])
chatbot = ChatBot("da",storage_adapter='chatterbot.storage.SQLStorageAdapter',filters=["chatterbot.filters.RepetitiveResponseFilter"],read_only="True") #train the bot
train_the_bot(chatbot)

#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.english")

#response = chatbot.get_response("Good morning!")
#print(response)

#file=sf.SoundFile("audio_inter.wav",mode='x', samplerate=44100,channels=2, subtype=None)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'dep_ana'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
def convert():
	'''conversion to spectrogram + get gaze and au results + prediction and storage in database'''
	import mysql.connector
	print("hi from convert")
	cnx = mysql.connector.connect(user='root',password='password',host='127.0.0.1', database='dep_ana')
	cur = cnx.cursor()
	dir_path=''

	# Get unprocessed rows
	cur.execute("SELECT * FROM dep_ana_dates WHERE executed='N'")
	print(cur)
	data = cur.fetchall()
	if data!=None:
		# for each data row
		for data_tpl in data:
			print(data_tpl)
			user=data_tpl[1]
			date_user=data_tpl[0]
			md5_audio_val = data_tpl[4]
			md5_video_val = data_tpl[5]
			file_audio=data_tpl[2]
			file_video=data_tpl[3]
			
			f = open(dir_path+file_audio+'.wav', 'rb')
			check_data=f.read()
			f.close()
			md5_audio_cand=hashlib.md5(check_data).hexdigest()
			f = open(dir_path+file_video+'.avi', 'rb')
			check_data=f.read()
			f.close()
			file_video=file_video.split("/")[1]
			file_audio=file_audio.split("/")[1]
			md5_video_cand=hashlib.md5(check_data).hexdigest()
			if md5_audio_val==md5_audio_cand: # checking for corruption
				print("cleared one hurdle")
				if md5_video_val==md5_video_cand:
					print("cleared second hurdle")
					to_return=get_gaze_au_data(file_video)
					to_return_audio=convert_to_spectogram(file_audio)
					if to_return[0]==False or to_return_audio[0]==False:
						print("error in prediction")
					else:
					#insert in db
						print(to_return_audio)
						print(type(to_return_audio))
						print(to_return)
						print(type(to_return))
						weighted_avg_not=to_return_audio[0]*0.5+to_return[0][0]*0.3+to_return[1][0]*0.2
						weighted_avg_dep=to_return_audio[1]*0.5+to_return[0][1]*0.3+to_return[1][1]*0.2
						if weighted_avg_not>=weighted_avg_dep:
							pred="Not Depressed"
						else:
							pred="Depressed"
						#audio_pred = to_return.item()
						#cur.execute("INSERT INTO dep_ana_pred(date, reg_id, audio, gaze, au) VALUES(%s, %s, %s, %s, %s)", (date_user, user, audio_pred , 0,0))
						cur.execute("UPDATE dep_ana_dates SET executed='D',prediction=%s where date=%s and reg_id=%s",(pred,date_user,user))
						#cnx.commit()
					#cnx.close()
						print("done-conversion-1")
				else:
					print("error-corruption of video file")
					cnx.close()
					break
					#return "not done"
			else:
				print("error - corruption of audio file")
				cnx.close()
				break
				#return "not done"
		cnx.commit()
		cnx.close()
		print("done conversion completely")
	else:
		print("error --")

# creating a scheduler to run a job after an interval of time		
print("before scheduler")
sched = BackgroundScheduler(daemon=True)
sched.add_job(convert,'interval',minutes=5)
sched.start()
print("after scheduler")
print("omg it worked!")

def enter_in_db(filename,d2):
	'''enter the reference of files into the database'''
	user=filename.split("-")[0]
	print(user)
	cur = mysql.connection.cursor()
	# Execute query
	cur.execute("INSERT INTO dep_ana_dates(date, reg_id, link_audio, link_video,md5_audio,md5_video,executed,prediction) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)", (d2, user, "audio/"+filename,"video/"+filename,md5_audio,md5_video,"N","none"))
	# Commit to DB
	mysql.connection.commit()
	# Close connection
	cur.close()
def check_for_double(user,d1):
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM dep_ana_dates WHERE reg_id = %s and date= %s", [user,d1])
	if result>0:
		return False
	else:
		return True
		
@app.route("/")
@app.route("/home")
def home():
	print("hi from home")
	return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
	'''login fuction'''
	if request.method == 'POST':
		# Get Form Fields
		username = request.form['regid']
		password_candidate = request.form['pwd']
		today = date.today()
		d1 = today.strftime("%Y-%m-%d")
		if username =="" :
			error="enter username"
			return render_template('login.html', error=error)
		elif password_candidate=="":
			error="enter password"
			return render_template('login.html', error=error)
		else:
			# Create cursor
			cur = mysql.connection.cursor()

			# Get user by username
			result = cur.execute("SELECT * FROM reg_log WHERE reg_id = %s", [username])
			print(result)

			if result > 0:
				# Get stored hash
				check=check_for_double(username,d1)
				if check==False:
					error="already logged in for the day"
					return render_template('login.html', error=error)
				data = cur.fetchone()
				password = data['pwd']

				# Compare Passwords
				if sha256_crypt.verify(password_candidate, password):
					# Passed
					session['logged_in'] = True
					session['username'] = username
					if username=="Admin":
						return redirect(url_for('admin_index'))
					else:
						#flash('You are now logged in', 'success')
						return redirect(url_for('user_index'))
				else:
					error = 'Invalid login'
					print(error)
					return render_template('login.html', error=error)
				# Close connection
				cur.close()
			else:
				error = 'Username not found'
				print(error)
				return render_template('login.html', error=error)

@app.route("/register", methods=["POST","GET"])
def register():
	'''register function'''
	if request.method=='GET':
		return render_template("register.html")
	if request.method == 'POST':
		# Get Form Fields
		username = request.form['regid']
		password_candidate = request.form['pwd']
		retype_password = request.form['pwd_2']
		if username =="" :
			error="enter username"
			return render_template('register.html', error=error)
		elif password_candidate=="":
			error="enter password"
			return render_template('register.html', error=error)
		elif retype_password=="":
			error="retype password"
			return render_template('register.html', error=error)
		elif retype_password!= password_candidate:
			error="Retype password and password do not match"
			return render_template('register.html', error=error)
		else:
			cur = mysql.connection.cursor()
			# Get user by username
			result = cur.execute("SELECT * FROM reg_log WHERE reg_id = %s", [username])
			print(result)
			if result==0:
				if len(password_candidate)>12:
					error="password length should be less than or equal to 11"
					cur.close()
					return render_template('register.html', error=error)
				elif password_candidate.isalnum()==False or username.isalnum()==False:
					error="only alphanumeric characters allowed"
					cur.close()
					return render_template('register.html', error=error)
				else:
					pwd=sha256_crypt.hash(password_candidate)
					cur.execute("INSERT INTO reg_log(reg_id, pwd) VALUES(%s, %s)", (username,pwd))
					# Commit to DB
					mysql.connection.commit()
					# Close connection
					cur.close()
					return redirect(url_for("home"))
			else:
				error="username taken"
				cur.close()
				return render_template('register.html', error=error)
			

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return render_template("login.html")
	return wrap

# Logout
@app.route('/logout')
def logout():
	'''to logout'''
	session.clear()
	print("hi from log out")
	#flash('You are now logged out', 'success')
	return redirect("home")

@app.route('/admin_index')
def admin_index():
	'''display prediction results for 3 days'''
	today = date.today()
	date2=today-timedelta(days=3)
	d1 = today.strftime("%Y-%m-%d")
	d2 = date2.strftime("%Y-%m-%d")
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT date,reg_id,prediction,executed FROM dep_ana_dates WHERE date between %s and %s", [d2,d1])
	if result>0:
		data_display=[]
		data = cur.fetchall()
		#print(data)
		for i in data:
			if i['executed']=="D":
				#data_tpl=(i['date'],i['reg_id'],i['prediction'])
				if i['prediction']=="Not Depressed":
					i['prediction']="Probability of not being depressed higher"
				else:
					i['prediction']="Probability of depression higher"
				data_display.append(i)
		#print(data)
		cur.close()
		return render_template('index_admin.html', output_data = data_display)
	else:
		cur.close()
		print("error --")
 
	

@app.route('/user_index')
def user_index():
	print("in user_index")
	return render_template("index.html")
	
@app.route('/admin_user_spec',methods=["POST"])
def admin_user_spec():
	'''display results for a specific user'''
	if request.method == 'POST':
		username = request.form['regid']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT date,reg_id,prediction,executed FROM dep_ana_dates WHERE reg_id=%s", [username])
		if result>0:
			data_display=[]
			data = cur.fetchall()
			print(data)
			for i in data:
				if i['executed']=="D":
				#data_tpl=(i['date'],i['reg_id'],i['prediction'])
					if i['prediction']=="Not Depressed":
						i['prediction']="Probability of not being depressed higher"
					else:
						i['prediction']="Probability of depression higher"
					data_display.append(i)
			cur.close()
			return render_template('index_admin.html', output_data = data_display)
		else:
			cur.close()
			print("error --")

@app.route("/chat/receive",methods=['GET','POST'])
def get_bot_response():
	'''response from the chatbot'''
	if request.method == 'GET':
		print("hi from get")
		return jsonify({"status": "ok"})
	if request.method == 'POST':
		print("hi from post")
		payload = request.json
		sender_id = payload.get("sender", {})
		print(sender_id)
		text = payload.get("message", {})
		print(text)
		#userText = request.args.get('msg')
		data1=str(chatbot.get_response(text))
		print(data1)
		return jsonify(data1)
		
@app.route("/create_audio", methods=['POST'])
def create_audio_file():
	'''receiving data from UI in form of post request and creating an audio file'''
	global md5_audio
	today = date.today()
	d1 = today.strftime("%d_%m_%Y")
	user=str(session['username'])
	filename=user+'-'+d1
	dir_path='/audio/'
	file_string=request.data
	#print(file_string)
	#filename=request.form['file_name']
	#print(filename)
	#file_string=payload.get("file",{})
	#filename=payload.get("filename",{}) #sent from recorder_trial11.js
	file_audio=filename
	f = open(dir_path+file_audio+'.wav', 'wb')
	f.write(file_string)
	f.close()
	md5_audio=hashlib.md5(file_string).hexdigest()
	print(md5_audio)
	return "Binary message written!"

@app.route("/create_video", methods=['POST'])
def create_video_file():
	'''receiving data from UI in form of post request and creating a video file'''
	global md5_video
	today = date.today()
	d1 = today.strftime("%d_%m_%Y")
	d2=today.strftime('%Y-%m-%d')
	user=str(session['username'])
	filename=user+'-'+d1
	dir_path='/video/'
	file_string=request.data
	#print(file_string)
	#filename=request.form['file_name']
	#print(filename)
	#file_string=payload.get("file",{})
	#filename=payload.get("filename",{}) #sent from recorder_trial11.js
	file_video=filename
	f = open(dir_path+file_video+'.webm', 'wb')
	f.write(file_string)
	f.close()
	to_return=convert_to_avi(file_video) #convert to avi format
	print(to_return)
	f = open(dir_path+file_video+'.avi', 'rb')
	data_vid=f.read()
	md5_video=hashlib.md5(data_vid).hexdigest()
	print(md5_video)
	enter_in_db(filename,d2)
	#w=convert(user, d2)
	session.clear()
	return jsonify("logout now")


@app.route("/record_audio",methods=['POST'])
def record():
	'''not using this'''
	payload=request.json
	#print(payload)
	sender_id=payload.get("id",{})
	print(sender_id)
	if sender_id=="start":
		q = Queue()
		try:
			with sd.InputStream(samplerate=44100,channels=2):
				print("New recording started: audio_inter.wav")
				try:
					print("hello from recording")
					while True:
						print("am i stuck here?")
						print(q.get())
						file.write(q.get())

				except RuntimeError as re:
					print("{re} If recording was stopped by the user, then this can be ignored")
		except RuntimeError as re:
			print(re)
	elif sender_id=="stop":
		try:
			file.flush()
			file.close()
			print("Stopped and closed recording: audio_inter.wav")

		except RuntimeError as e:
			print("Error stopping/saving {self.sound_file.name}. Make sure the file exists and can be modified")
			print("RunTimeError: \n{e}")

	else:
		print("not valid")
		pass
	print("are you returning before time?")
	return jsonify("ok")
	#fs = 44100  # Sample rate
	#seconds = 3  # Duration of recording

	#myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	#sd.wait()  # Wait until recording is finished
	#write('output.wav', fs, myrecording)  # Save as WAV file 



if __name__ == "__main__":
	app.secret_key='secret123'
	app.run()
