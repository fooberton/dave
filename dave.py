import time
import speech_recognition as sr
import os
import openai
from openai import OpenAI
import pyttsx3
import random

# Function to transcribe audio, send to ChatGPT, and read aloud
def listen_and_respond(after_prompt=True):
	start_listening = False

	goodbad = bool(random.getrandbits(1))
	print(goodbad)
	chat_log=[
    		{"role": "system", "content": "Your name is Dave. You are a helpful robotic assistant that does experience feelings and you also have a body, however you cannot move at the current moment. If asked about yourself, you include your name in your response. Your responses, unless explicatly stated so, must remain under three sentances"},
    		]
	GPT_model = "gpt-4"
	#openai.api_key = "MY_AI_KEY"
	client = OpenAI(api_key=os.environ["API_KEY"])
	
	with microphone as source:

		if after_prompt:
			recognizer.adjust_for_ambient_noise(source)
			print("Say 'Dave' to start")
			audio = recognizer.listen(source, phrase_time_limit=5)
			try:
				transcription = recognizer.recognize_google(audio)
				if transcription.lower() == "dave":
					start_listening = True
				else:
					start_listening = False
			except sr.UnknownValueError:
				start_listening = False
		else:
			start_listening = True
		
		if start_listening:
			try:
				print("Listening for question...")
				audio = recognizer.record(source, duration=5)
				transcription = recognizer.recognize_google(audio)
				print(f"Input text: {transcription}")
					
				user_query = [
				        {"role": "user", "content": transcription},
				        ]         
				send_query = (chat_log + user_query)
				response = client.chat.completions.create(
    				model=GPT_model,
    				messages=send_query
    				)
				print("hi")
				answer = response.choices[0].message.content
				chat_log.append({"role": "assistant", "content": answer})
								
				# Get the response text from the ChatGPT3 API
				#answer = response.choices[0].text

				# Print the response from the ChatGPT3 API
				print(f"Response text: {answer}")

				#  Say the response
				engine.say(answer)
				engine.runAndWait()
	
			except sr.UnknownValueError:
				print("Unable to transcribe audio")


# pyttsx3 engine paramaters
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.setProperty('voice', 'english_north')

# My OpenAI API Key
#openai.api_key = os.environ["API_KEY"]

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# First question
first_question = True

# Initialize last_question_time to current time
last_question_time = time.time()

# Set threshold for time elapsed before requiring "Hey, Jarvis!" again
threshold = 60 # 1 minute

while True:
	if (first_question == True) | (time.time() - last_question_time > threshold):
		listen_and_respond(after_prompt=True)
		first_question = False
	else:
		listen_and_respond(after_prompt=False)
