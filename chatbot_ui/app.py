import os
import sys
import pylab
import wave
from flask import Flask, render_template, request,jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from train import train_the_bot
from con_specto import convert_to_spectogram
from converter import Converter
from vid_avi import convert_to_avi
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
from queue import Queue 
from stat import S_ISREG, ST_CTIME, ST_MODE


chatbot = ChatBot("dontstopmenow")
train_the_bot(chatbot)
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.english")

response = chatbot.get_response("Good morning!")
print(response)

#file=sf.SoundFile("audio_inter.wav",mode='x', samplerate=44100,channels=2, subtype=None)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat/receive",methods=['GET','POST'])
def get_bot_response():
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

@app.route("/convert", methods=['POST'])
def convert():
	#file_name=
	#a=[]
	dir_path='C:/Users/vandi/Documents/final_year_proj/'
	payload=request.json
	filename=payload.get("message",{})
	file_audio=dir_path+'audio/'+filename+'.wav'
	file_vid=dir_path+'video/'+filename+'.webm'
	to_return=convert_to_avi(file_vid)
	print(to_return)
	to_return=str(convert_to_spectogram(file_audio))
	return(jsonify(to_return))

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
    app.run()
