__author__ = "Ajay Prakash"
__email__ = "ajayprakashk7@gmail.com"
__copyright__ = "Copyright (C) 2023 by Ajay Prakash"
__license__ = "MIT License"
__version__ = "1.0.0"
import openai
import os
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# settings and keys
openai.api_key = "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"
model_engine = "text-davinci-002"
language = 'en'

def recognize_speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        # convert the audio to text
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        speech = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speech = ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        speech = ""

    return speech

def chatgpt_response(prompt):
    # send the converted audio text to chatgpt
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=64, # Reduce the number of tokens to speed up the response time
        n=1,
        temperature=0.7,
    )
    return response

def generate_audio_file(text):
    # convert the text response from chatgpt to an audio file 
    audio = gTTS(text=text, lang=language, slow=False)
    # save the audio file
    audio.save("response.mp3")

def play_audio_file():
    # play the audio file
    os.system("mpg321 response.mp3")
    playsound("response.mp3", block=False) # There’s an optional second argument, block, which is set to True by default. Setting it to False makes the function run asynchronously.

def main():
    developer_name = "Ajay Prakash"
    # run the program in a loop
    while True:
        prompt = recognize_speech()
        print(f"This is the prompt being sent to OpenAI: " + prompt)
        if prompt == "":
            continue
        if "introduce yourself" in prompt.lower():
            generate_audio_file(f"Hello, I am a chatbot created by {developer_name}")
            play_audio_file()
            continue
        responses = chatgpt_response(prompt)
        message = responses.choices[0].text
        print(message)
        generate_audio_file(message)
        play_audio_file()

if __name__ == "__main__":
    main()
