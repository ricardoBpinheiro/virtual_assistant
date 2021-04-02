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

# Ignore any warning messages
warnings.filterwarnings('ignore')


# Record audio and return a string
def record_audio():
    r = sr.Recognizer()  # Creating a recognize object

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print('Fale Algo:')
        audio = r.listen(source)

    # Use Google speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('Você falou: ' + data)
    except sr.UnknownValueError:  # The reconignition dont understand the message
        print('Google não reconheceu a sua fala')
    except sr.RequestError as e:
        print('Service Erro: ' + e)

    return data


def assistant_response(text):
    # print(text)
    # Convert the text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    print('Alexa2: ' + text)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    # Play the converted file
    os.system('start assistant_response.mp3')


# Function for wake word(s) or phrase
def wake_word(text):
    wake_words = ['hey computer', 'gutty', 'hello', 'mango', 'hey alexa']
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
    greeting_inputs = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']

    # Greeting responses
    greeting_responses = ['Hello human, i am alexa 2,', 'Hello, Im robot, ', 'Hello, ', 'Hi, ', 'Ricardo is beautiful, ']

    for word in text.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)

    # If no greeting was detected then return as empty string
    return ''


# A function to get a persons first and last name from the text
def get_person(text):
    word_list = text.split()

    for i in range(0, len(word_list)):
        if i + 3 <= len(word_list) - 1 and word_list[i].lower() == 'who' and word_list[i+1].lower() == 'is':
            return word_list[i+2] + ' ' + word_list[i+3]


while True:
    # Record the audio
    text = record_audio()
    response = ''

    # Check for the wake word
    if wake_word(text) is True:
        # print('Me chamou mestre?')

        # Check for greetings by the user
        response = response + greeting(text)

        # Check if user said date
        if 'date' in text:
            get_date = get_date()
            response = f'{response} {get_date}'

        if 'time' in text:
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

            response = f'{response} It is {str(hour)} : {minute} {meridiem}.'

        # Check if user said who is
        if 'who is' in text:
            person = get_person(text)
            print(person)
            wiki = wikipedia.summary(person, sentences=2)
            response = f'{response} {wiki}'

        # Have the assistant respond back using audio and the text from response
        assistant_response(response)


# text = 'Gutty is top'
# assistant_response(text)












