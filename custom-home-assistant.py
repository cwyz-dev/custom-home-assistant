#   Description:
#       Based off the base code from an article on medium.com. (medium.com/@randerson112358/build-a-virtual-assistant-using-python-2b0f78e68b94)

WAKE_WORDS = ['computer']

from gtts import gTTS
import os
import pyaudio
import speech_recognition as sr

import GoogleTextAssistant

# Record audio and return it as a string
# Almost exactly copied from the article.
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as audioInput:
        print('Say something...')
        audio = r.listen(audioInput)

    data = ''
    try:
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand.')
    except sr.RequestError as e:
        print('Request error from Google Speech Recognition.')
    return data

# Function to check for wake word(s)
def wakeWord(text):
    for phrase in WAKE_WORDS:
        if phrase.lower() in text:
            return True
    return False

# Function to remove wake word(s) from the beginning
def removeWakeWord(text):
    for phrase in WAKE_WORDS:
        if text[0:len(phrase):] == phrase.lower():
            return text[len(phrase)+1:]
    return text

def askGoogle(query):
    print('Asking Google: ' + query)
    with GoogleTextAssistant('en-CA', device_model_id, device_id, False, grpc_channel, 185) as assistant:
        response_text, response_html = assistant.assist(query)
        if response_text:
            print(response_text)

ASKS = {"google":askGoogle}

def askCommand(who, content):
    ASKS[who](content)

COMMANDS = {"ask":askCommand}

# Function to call different commands
def callCommand(text):
    items = text.lower().split(' ')
    if items[0] in COMMANDS:
        COMMANDS[items[0]](items[1], text[len(items[0])+len(items[1])+2:])

if __name__ == '__main__':
    while True:
        text = recordAudio()
        if (len(text) > 0):
            if wakeWord(text):
                text = removeWakeWord(text)
                print('You said: ' + text)
                callCommand(text)
