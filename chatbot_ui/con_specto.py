#from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
#need to import
import os
import sys
import pylab
import wave
import json
import numpy as np
import keras
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import model_from_json
import tensorflow
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from PIL import Image
import os
import time


def convert_to_spectogram(file_name):
	#file_name="audio_inter"
	path='C:/Users/vandi/Documents/final_year_proj/audio/'
	#a=os.listdir(path)
	#print(a)
	w=wave.open(path+file_name+'.wav','rb')
	frames = w.readframes(-1)
	sound_info = pylab.frombuffer(frames, 'Int16')
	frame_rate = w.getframerate()
	w.close()
	pylab.figure(num=None, figsize=(15, 15))
	pylab.subplot(111)
	pylab.title('spectrogram of the audio file')
	pylab.specgram(sound_info, Fs=frame_rate)
#     pylab.savefig('spectrogram.png')
	pylab.savefig('C:/Users/vandi/Documents/final_year_proj/spectogram/'+file_name+'_spec.png')
	dim=(512,512)
	img=Image.open('C:/Users/vandi/Documents/final_year_proj/spectogram/'+file_name+'_spec.png')
	new_img = img.resize(dim, Image.ANTIALIAS)
	new_img.save('C:/Users/vandi/Documents/final_year_proj/spectogram_test/'+file_name+'_spec.png')
	file_name+='_spec.png'
	prediction=prediction_using_cnn(file_name)
	if prediction is not None:
		return prediction[0][1]
	else:
		return False

def prediction_using_cnn(file_name):
	arr=[]
	json_file = open('C:/Users/vandi/Documents/final_year_proj/chatbot_ui/audio_model/audio.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
		loaded_model = model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("C:/Users/vandi/Documents/final_year_proj/chatbot_ui/audio_model/audio.h5")
		t=load_img('C:/Users/vandi/Documents/final_year_proj/spectogram_test/'+file_name)
		x=img_to_array(t)
		arr.append(x)
		prediction=loaded_model.predict(np.array(arr))
		return(prediction)

#prediction=prediction_using_cnn("346_AUDIO_spec.png")
#print(prediction)

#print(convert_to_spectogram("xyz"))