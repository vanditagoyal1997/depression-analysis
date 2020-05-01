import os
from os import listdir
from os.path import isfile, join
from vid_avi import convert_to_avi
import subprocess
import pandas as pd
def separate_data(file_video):
	path_data="C:\\Users\\vandi\\Documents\\final_year_proj\\chatbot_ui\\processed\\"+file_video+".csv"
	au_path="C:\\Users\\vandi\\Documents\\final_year_proj\\au_data\\"+file_video+"_CLNF_AU.csv"
	data = pd.read_csv(path_data)
	final_au_df = data[['frame','timestamp','confidence','success','AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU09_r', 'AU10_r', 'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 'AU25_r', 'AU26_r', 'AU04_c', 'AU12_c', 'AU15_c', 'AU23_c', 'AU28_c', 'AU45_c']]
	final_au_df.to_csv(au_path , index = False)


def get_gaze_au_data(file_video):
	print("hi from gaze_au")
	for i in range(0,50000):
		print("delay")
	path="C:\\Users\\vandi\\Documents\\final_year_proj\\OpenFace_2.2.0_win_x64\\OpenFace_2.2.0_win_x64\\FeatureExtraction.exe"
	file_path=r'C:\\Users\\vandi\\Documents\\final_year_proj\\video\\'
	convert_to_avi(file_video)
	#path2=os.getcwd()
	args=path+' -f '+'"'+file_path+file_video+'.avi'
	print(args)
	temp=subprocess.call(args)
	
	return("ok...processed")
#print(temp.stdout.read())
#get_gaze_au_data("2020-04-27T08_47_00.000Z")