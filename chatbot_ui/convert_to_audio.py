import base64
def base64_decode(s):
	"""Add missing padding to string and return the decoded base64 string."""
	#log = logging.getLogger()
	s = str(s).strip()
	try:
		return base64.b64decode(s)
	except TypeError:
		print("hi from exception")
		padding = len(s) % 4
		if padding == 1:
			print("Invalid base64 string: {}".format(s))
			return ''
		elif padding == 2:
			s += b'=='
		elif padding == 3:
			s += b'='
		return base64.b64decode(s)

def convert_aud(file_name,str_64):
	dir_path='C:/Users/vandi/Documents/final_year_proj/audio/'
	wav_file = open(dir_path+file_name+".wav", "wb")
	str_64=str_64.replace("%3D","=")
	decode_string = base64.urlsafe_b64decode(str_64)
	wav_file.write(decode_string)
	print("converted to audio")
