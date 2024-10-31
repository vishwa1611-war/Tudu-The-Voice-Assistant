import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import smtplib
import wikipediaapi
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')

# Get the list of available voices and set the preferred voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to female voice, change index if needed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("Sir! I am Tudu. How can I assist you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Using Google for voice recognition
        print(f"User said: {query}\n")  # User query will be printed
    except Exception as e:
        print(e)
        print("Say that again please...")  # Say that again will be printed in case of improper voice
        return "None"  # None string will be returned
    return query

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Use environment variables or a safer method to handle passwords
        server.login('vishwajeeth2014@gmail.com', '###password--') 
        server.sendmail('bavithshetty15@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email.")

def getWeather(city="Mangalore"):
    api_key = "7a1f7fdc624e417700931624c84c6c0e"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Check if the request was successful
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"] - 273.15  # Convert from Kelvin to Celsius
            weather_description = x["weather"][0]["description"]
            speak(f"The temperature in {city} is {current_temperature:.2f} degrees Celsius with {weather_description}.")
        else:
            speak("City not found")
    except requests.exceptions.RequestException as e:
        print(e)
        speak("Sorry, I am not able to fetch the weather information.")

def search_wikipedia(query):
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(query)
    if page.exists():
        summary = page.summary[:500]  # Fetch the first 500 characters of the summary
        return summary
    else:
        return "No Wikipedia page found for this query."

# Spotify Setup
def play_on_spotify(song_name):
    # Search for the song on Spotify
    result = sp.search(q=song_name, type='track')
    track_uri = result['tracks']['items'][0]['uri']
    
    # Get available devices
    devices = sp.devices()
    if len(devices['devices']) > 0:
        device_id = devices['devices'][0]['id']  # Use the first available device or select manually
        
        # Play the song on the selected device
        sp.start_playback(device_id=device_id, uris=[track_uri])
    else:
        print("No active device found. Please open Spotify on one of your devices.")


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()  # Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = search_wikipedia(query)
            speak("According to Wikipedia")
            print(results)
            speak(results)
       
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        
        elif 'hi tudu' in query:
            speak("Hi! Thank you for waking me up! How can I assist you?")
        
        elif 'open whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com/")
        
        elif 'play music' in query:
            music_file = 'F:\\public\\Projects\\jarvis\\titanium-170190.mp3'
            try:
                if os.path.isfile(music_file):
                    os.startfile(music_file)
                    speak("Playing music")
                else:
                    speak("Music file not found")
            except Exception as e:
                print(e)
                speak("An error occurred while trying to play music")
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif 'the date' in query:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {today}")
        
        elif 'weather' in query:
            getWeather()

        # Play a song on Spotify
        elif 'play' in query and 'on spotify' in query:
            song_name = query.replace('play', '').replace('on spotify', '').strip()
            play_on_spotify(song_name)
           


        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "vishwajeeth2014@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to process your request.")
        
        elif 'bye' in query:
            speak("Goodbye!")
            break
