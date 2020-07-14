
# Process Flow for application

1.	User logs in
2.	User chats with the chatbot. The speech input is converted into text using WebSpeech API
3.	The text input is then given to the chatbot which responds. The response is converted back into speech. 
4.	When the user is done, he can stop recording. He will be automatically logged out.
5.	Meanwhile, the video and the audio are being recorded and is stored in the database. 
6.	A scheduled job runs every hour to process the audio and video file
7.	It takes the audio file and converts it into a spectrogram
8.	The video file is processed by OpenFace software to provide Gaze and “Action units” data
9.	These data files are then sent to the model for prediction.
10.	The predictions are stored in the database
11.	The counsellor can log in and view the results through the User Interface.

# Flow diagram for application
![Flow diagram] (/images/ui_multi.jpg)
