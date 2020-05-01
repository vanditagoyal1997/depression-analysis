import requests


url = "https://www23.online-convert.com/dl/web7/upload-file/f945d4e8-9482-437c-b3e7-e36c73c87af8"

payload = {}
files = [
  ('file', open('C:/Users/vandi/Documents/final_year_proj/audio/2020-04-27T08_47_00.000Z.webm','rb'))
]
headers = {
  'x-oc-api-key': '766087c1443d59794c0a2d31e8529644'
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))

url = "https://api2.online-convert.com/jobs"

payload = "{\r\n    \"conversion\": [{\r\n        \"category\": \"video\",\r\n        \"target\": \"avi\"\r\n    }]\r\n}"
headers = {
  'x-oc-api-key': '766087c1443d59794c0a2d31e8529644',
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

url = "https://www23.online-convert.com/dl/web7/download-file/5fbe1d6e-ab1e-4487-a406-bfd658ff4f2c/2020-04-24T19_00_00.000Z.avi"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
