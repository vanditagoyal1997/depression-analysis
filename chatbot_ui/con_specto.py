#from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
import sys
import pylab
import wave

def convert_to_spectogram(file_name):
	path='C:/Users/vandi/Documents/final_year_proj/audio/'
	w=wave.open(path+file_name,'rb')
	frames = w.readframes(-1)
	sound_info = pylab.frombuffer(frames, 'Int16')
	frame_rate = w.getframerate()
	w.close()
	pylab.figure(num=None, figsize=(15, 15))
	pylab.subplot(111)
	pylab.title('spectrogram of the audio file')
	pylab.specgram(sound_info, Fs=frame_rate)
#     pylab.savefig('spectrogram.png')
	pylab.savefig('C:/Users/vandi/Documents/final_year_proj/spectogram_test/'+file_name+'_spec.png')
	return True