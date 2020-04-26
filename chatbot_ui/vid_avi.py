#for conversion to avi
from converter import Converter
def convert_to_avi(file_video):
	conv = Converter()
	to_file=file_video[:-5]+'.avi'
	convert = conv.convert(file_video, to_file, {
    'format': 'avi',
        'video': {
        'width': 640,
        'height': 480
    }})
	return ('ok...converted video')

convert_to_avi("C:\\Users\\vandi\\Downloads\\2020-04-20T12_20_06.030Z.webm")