import os
from os import listdir
from os.path import isfile, join
from vid_avi import convert_to_avi
import subprocess
import pandas as pd
import numpy as np
import keras
import tensorflow as tf
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from random import randint
pd.options.mode.chained_assignment = None 
val=randint(315,317) 
path_data1="C:\\Users\\vandi\\Documents\\final_year_proj\\chatbot_ui\\processed\\"+str(val)+"_CLNF_gaze.txt"
path_data2="C:\\Users\\vandi\\Documents\\final_year_proj\\chatbot_ui\\processed\\319_CLNF_gaze.txt"
def au_data_pred(file_video):
	flag=[]
	table=[]
	path_data="C:\\Users\\vandi\\Documents\\final_year_proj\\chatbot_ui\\processed\\"+file_video+".csv"
	au_path="C:\\Users\\vandi\\Documents\\final_year_proj\\au_data\\"+file_video+"_CLNF_AU.txt"
	gaze_path="C:\\Users\\vandi\\Documents\\final_year_proj\\gaze_data\\"+file_video+"_CLNF_gaze.txt"
	data = pd.read_csv(path_data)
	final_au_df = data[[" success"," AU01_r"," AU02_r"," AU04_r"," AU05_r"," AU06_r"," AU09_r"," AU10_r"," AU12_r"," AU14_r"," AU15_r"," AU17_r"," AU20_r"," AU25_r"," AU26_r"]]
	final_au_df.to_csv(au_path ,sep=',', index = False)
	final_au_df=pd.read_table(au_path,sep=",")
	t=final_au_df.iloc[:,1:18]
	#print(t)
  # t=df[[" AU01_r"," AU04_r"," AU15_r"]]
	my_list=[]
	for index, rows in t.iterrows(): 
      # Create list for the current row 
		my_list =[rows[' AU01_r'],rows[' AU02_r'],rows[' AU04_r'],rows[' AU05_r'],rows[' AU06_r'],rows[' AU09_r'],rows[' AU10_r'],rows[' AU12_r'],
                rows[' AU14_r'],rows[' AU15_r'],rows[' AU17_r'],rows[' AU20_r'],rows[' AU25_r'],rows[' AU26_r'],] 
        
      # append the list to the final list 
		flag.append(my_list)
	#counter=counter+1
	table.append(flag)
	np.array(table)
	padded_au=pad_sequences(table,padding='post')
	json_file = open('C:/Users/vandi/Documents/final_year_proj/chatbot_ui/au_model/au.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
		loaded_model = tf.keras.models.model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("C:/Users/vandi/Documents/final_year_proj/chatbot_ui/au_model/au.h5")
		prediction=loaded_model.predict(padded_au)
		return prediction[0]
	#final_gaze_df=data[['frame',' timestamp',' confidence',' success',' gaze_0_x',' gaze_0_y',' gaze_0_z',' gaze_1_x',' gaze_1_y',' gaze_1_z']]
	#final_gaze_df.rename(columns = {' gaze_0_x':'x_0', ' gaze_0_y':'y_0', ' gaze_0_z':'z_0',' gaze_1_x':'x_1',' gaze_1_y':'y_1',' gaze_1_z':'z_1'}, inplace = True) 
	#final_gaze_df.to_csv(gaze_path ,sep=',', index = False)

def gaze_data_pred(file_video):
	flag=[]
	table=[]
	path_data="C:\\Users\\vandi\\Documents\\final_year_proj\\chatbot_ui\\processed\\"+file_video+".csv"
	gaze_path="C:\\Users\\vandi\\Documents\\final_year_proj\\gaze_data\\"+file_video+"_CLNF_gaze.txt"
	data = pd.read_csv(path_data2)
	final_gaze_df=data[[' success',' x_0',' y_0',' z_0',' x_1',' y_1',' z_1',' x_h0',' y_h0',' z_h0',' x_h1',' y_h1',' z_h1']]
	final_gaze_df.to_csv(gaze_path ,sep=',', index = False)
	final_gaze_df=pd.read_table(gaze_path,sep=",")
	t=final_gaze_df.iloc[:,0:16]
	t.rename(columns={' success':'success',' x_0':'x_0',' y_0':'y_0',' z_0':'z_0',' x_1':'x_1',' y_1':'y_1',' z_1':'z_1',
                    ' x_h0':'x_h0',' y_h0':'y_h0',' z_h0':'z_h0',' x_h1':'x_h1',' y_h1':'y_h1',' z_h1':'z_h1'},inplace=True)
	my_list=[]
	for index, rows in t.iterrows(): 
      # Create list for the current row 
		my_list =[rows.success,rows.x_0, rows.y_0, rows.z_0,rows.x_1, rows.y_1, rows.z_1,
                rows.success,rows.x_h0, rows.y_h0, rows.z_h0,rows.x_h1, rows.y_h1, rows.z_h1] 
        
      # append the list to the final list 
		flag.append(my_list)
  # print('check')
	table.append(flag)
	np.array(table)
	padded_gaze=pad_sequences(table,padding='post')
	json_file = open('C:/Users/vandi/Documents/final_year_proj/chatbot_ui/gaze_model/gaze.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
		loaded_model = tf.keras.models.model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("C:/Users/vandi/Documents/final_year_proj/chatbot_ui/gaze_model/gaze.h5")
		prediction=loaded_model.predict(padded_gaze)
		return prediction[0]
	
def get_gaze_au_data(file_video):
	print("hi from gaze_au")
	path="C:\\Users\\vandi\\Documents\\final_year_proj\\OpenFace_2.2.0_win_x64\\OpenFace_2.2.0_win_x64\\FeatureExtraction.exe"
	file_path=r'C:\\Users\\vandi\\Documents\\final_year_proj\\video\\'
	#convert_to_avi(file_video)
	#path2=os.getcwd()
	args=path+' -f '+'"'+file_path+file_video+'.avi'
	print(args)
	temp=subprocess.call(args)
	#separate_data(file_video)
	au_pred=au_data_pred(file_video)
	gaze_pred=gaze_data_pred(file_video)
	au_pred=np.array(au_pred).tolist()
	gaze_pred=np.array(gaze_pred).tolist()
	pred_list=[au_pred,gaze_pred]
	if au_pred is not None:
		if gaze_pred is not None:
			return pred_list
		else:
			return [False]
	else:
		return [False]
	
#print(temp.stdout.read())
# a=get_gaze_au_data("2016ucp1004-03_05_2020")
# print(type(a))
# print(a)
# print(type(a[0]))
# print(type(a[1]))