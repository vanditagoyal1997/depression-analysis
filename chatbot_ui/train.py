from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
#from chatterbot.trainers import ChatterBotCorpusTrainer

def train_the_bot(chatbot_name):
	trainer = ListTrainer(chatbot_name)
	trainer.train([
	"Hello",
    "Hi! How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome."
	])
	trainer.train([
	"Hello",
    "Hi! How are you?",
    "I am not feeling fine.",
    "I feel very sad to hear that. Why do you feel so?",
    "I failed my exam today.",
    "It is alright. You will pass the next time!",
	"Thank you for saying that",
	"You are welcome"
	])
	trainer.train([
	"Hello",
    "Hi! How are you?",
    "I am fine.",
    "That is good to hear.",
    "Thank you",
	"So what is your favorite colour?",
	"blue",
	"where are you from originally?",
	"Noida",
	"Why did you move to a college in jaipur then?",
	"Because i wanted to be close to home yet far enough from it"
	])
	

