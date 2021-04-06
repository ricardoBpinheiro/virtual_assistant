# pip install pyaudio
# pip install SpeechRecognition
# pip install gTTS
# pip install wikipedia

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import platform

# Ignore any warning messages
warnings.filterwarnings('ignore')


# Record audio and return a string
def record_audio():
    r = sr.Recognizer()  # Creating a recognize object

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print('Fale Algo:')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Use Google speech recognition
    data = ''
    try:
        data = r.recognize_google(audio, language='pt-br')
        print('Você falou: ' + data)
    except sr.UnknownValueError:  # The reconignition dont understand the message
        print('Google não reconheceu a sua fala')
    except sr.RequestError as e:
        print('Service Erro: ' + e)

    return data


def assistant_response(text):
    # print(text)
    # Convert the text to speech
    if text is not '':
        myobj = gTTS(text=text, lang='pt-br', slow=False)

        print('Alexa2: ' + text)

        # Save the converted audio to a file
        myobj.save('assistant_response.mp3')

        # Play the converted file
        if platform.system() is 'Windows':
            os.system('start assistant_response.mp3')
        else:
            os.system('nvlc assistant_response.mp3')


# Function for wake word(s) or phrase
def wake_word(text):
    wake_words = ['oi', 'hi', 'gutty', 'Olá', 'tudo bem', 'hey alexa']
    text = text.lower()

    # Validate the text = voice command
    for phrase in wake_words:
        if phrase in text:
            return True
    # If the wake word isn't found in the text from the loop and so it returns false
    return False


# Function to get the current date
def get_date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    week_day = my_date.isoweekday()
    month_num = now.month
    day_num = now.day
    year_num = now.year

    # List of months
    month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # List of week days
    week_day_names = ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado']

    # A list of ordinal numbers
    ordinal_numbers = ['1°', '2°', '3°', '4°', '5°', '6°', '7°', '8°', '9°', '10°',
                       '11°', '12°', '13°', '14°', '15°', '16°', '17°', '18°', '19°', '20°',
                       '21°', '22°', '23°', '24°', '25°', '26°' '27°', '28°', '28°', '29°', '30°', '31°']

    return f'Hoje é dia {ordinal_numbers[day_num - 1]}, uma {week_day_names[week_day]}, mês de {month_names[month_num - 1]}, ano {year_num}.'


# A function to return a random greeting response
def greeting(text):
    # Greeting Inputs
    greeting_inputs = ['oi', 'Olá', 'tudo bem']

    # Greeting responses
    greeting_responses = ['Olá humano, eu sou a alexa 2,', 'Olá, Eu sou um robô, ', 'Olá, ', 'Oi, ', 'Ricardo é lindo, ']

    for word in text.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)

    # If no greeting was detected then return as empty string
    return ''


# A function to get a persons first and last name from the text
def get_person(text):
    word_list = text.split()

    for i in range(0, len(word_list)):
        if i + 3 <= len(word_list) - 1 and word_list[i].lower() == 'quem' and word_list[i+1].lower() == 'é':
            return word_list[i+2] + ' ' + word_list[i+3]


while True:
    # Record the audio
    text = record_audio()
    response = ''
    # Check for the wake word
    if wake_word(text) is True:
        # print('Me chamou mestre?')
        print(text)
        # Check for greetings by the user
        response = response + greeting(text)

        # Check if user said date
        if 'dia' in text:
            get_date = get_date()
            response = f'{response} {get_date}'

        if 'tempo' in text:
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'p.m'
                hour = now.hour - 12
            else:
                meridiem = 'a.m'
                hour = now.hour

            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)

            response = f'{response} É {str(hour)} : {minute} {meridiem}.'

        # Check if user said who is
        if 'quem é' in text:
            person = get_person(text)
            print(person)
            wiki = wikipedia.summary(person, sentences=2)
            response = f'{response} {wiki}'

        # Have the assistant respond back using audio and the text from response
        print(response)
        assistant_response(response)


# text = 'Gutty is top'
# assistant_response(text)
