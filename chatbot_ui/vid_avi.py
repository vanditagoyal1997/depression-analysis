#for conversion to avi
#from converter import Converter
import os
def convert_to_avi(file_video):
	path_orig="C:\\Users\\vandi\\Documents\\final_year_proj\\audio\\"
	path_final="C:\\Users\\vandi\\Documents\\final_year_proj\\video\\"
	string_arg='ffmpeg -i '+'"'+path_orig+file_video+".webm"+'"'+' '+'"'+path_final+file_video+".avi"+'"'
	os.system('cmd /c '+'"'+string_arg+'"') 
	# conv = Converter()
	# to_file=file_video[:-5]+'.avi'
	# convert = conv.convert(file_video, to_file, {
    # 'format': 'avi',
        # 'video': {
        # 'width': 640,
        # 'height': 480
    # }})
	# return ('ok...converted video')

#convert_to_avi("C:\\Users\\vandi\\Documents\\final_year_proj\\audio\\2020-04-27T08_47_00.000Z.webm")