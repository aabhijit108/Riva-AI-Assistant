import os
import time
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import requests
from bs4 import BeautifulSoup
import win32com.client as wincl
from win32com.client import Dispatch
import pythoncom
from plyer import notification
import winshell
import re
import glob
import urllib.parse
import tempfile
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import openai
import shutil
from openrouter_helper import ask_openrouter
import shutil
from pdf_reader import read_document


# Initialize Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="eb662e5f26f84f78a7a371d44c5be00b",
    client_secret="94e58854711042e79a1d500522c752ca",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))

# Text-to-speech
def speak(text):
    pythoncom.CoInitialize()
    for sentence in text.split('. '):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() and ("india" in voice.name.lower() or "en-in" in voice.id.lower()):
                engine.setProperty('voice', voice.id)
                break
        else:
            engine.setProperty('voice', voices[1].id)

        engine.setProperty('rate', 140)
        engine.setProperty('volume', 1.0)
        engine.say(sentence)
        engine.runAndWait()
        engine.stop()

# Wake word
WAKE_WORDS = ["hi riva", "hello riva", "riva", "hello"]

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        print("Please repeat...")
        return "None"

def listen_for_wake_word():
    while True:
        query = take_command()
        if any(wake in query for wake in WAKE_WORDS):
            speak("Yes Abhijit Sir?")
            return

# Greeting
def get_greeting():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

# File/folder actions
def create_file(file_name, file_type):
    try:
        if file_type == "folder":
            os.makedirs(file_name)
        else:
            with open(f"{file_name}.{file_type}", 'w'):
                pass
        speak(f"Created {file_type} {file_name}")
    except Exception as e:
        speak(str(e))

def delete_file(file_path):
    try:
        if os.path.isdir(file_path):
            winshell.delete_folder(file_path)
        else:
            winshell.delete_file(file_path)
        speak("Deleted successfully")
    except Exception as e:
        speak(str(e))

def restore_from_recycle_bin(item_name):
    try:
        recycle_bin = winshell.recycle_bin()
        for item in recycle_bin:
            if item_name.lower() in item.original_filename().lower():
                winshell.undelete(item.original_filename())
                speak(f"Restored {item_name}")
                return
        speak("Not found")
    except Exception as e:
        speak(str(e))

# Open apps
def open_application(app_name):
    logs = []
    apps = {
        'chrome': 'chrome.exe', 'edge': 'msedge.exe', 'firefox': 'firefox.exe',
        'calculator': 'calc.exe', 'calendar': 'outlookcal:',
        'vs code': 'code.exe', 'notepad': 'notepad.exe', 'notepad++': 'notepad++.exe',
        'android studio': 'studio64.exe', 'camera': 'microsoft.windows.camera:',
        'mail': 'outlookmail:', 'settings': 'ms-settings:', 'control panel': 'control.exe'
    }
    try:
        if app_name in apps:
            os.system(f'start {apps[app_name]}')
            speak(f"Opening {app_name}")
            logs.append(f"Opening {app_name}")
        else:
            speak("App not recognized")
    except Exception as e:
        speak(str(e))

# Music on Spotify

def play_music(song_name):
    try:
        query = urllib.parse.quote(song_name)
        url = f"https://open.spotify.com/search/{query}"
        webbrowser.open(url)
        speak(f"Searching {song_name} on Spotify")
    except Exception as e:
        speak(str(e))

# Other actions

def search_anything(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Results for {query}")

def get_weather(city):
    logs = []
    try:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=37a172e63e0bba065e093813c2330d07&units=metric"
        data = requests.get(base_url).json()
        if data["cod"] != "404":
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"{city} weather: {weather}, {temp}°C")
            logs.append(f"{city} weather: {weather}, {temp}°C")
    except:
        speak("Failed to get weather")
        logs.append("Failed to get weather")

# Function to get product price
def get_product_price(product_name, website="amazon"):
    logs = []
    try:
        if website == "amazon":
            url = f"https://www.amazon.in/s?k={product_name}"
        else:
            url = f"https://www.flipkart.com/search?q={product_name}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if website == "amazon":
            price = soup.find('span', {'class': 'a-price-whole'})
        else:
            price = soup.find('div', {'class': '_30jeq3'})
        
        if price:
            speak(f"The price of {product_name} on {website} is approximately {price.text}")
            logs.append(f"The price of {product_name} on {website} is approximately {price.text}")
        else:
            speak(f"Couldn't find the price for {product_name} on {website}")
            logs.append(f"Couldn't find the price for {product_name} on {website}")
    except Exception as e:
        speak(f"Sorry, I couldn't fetch the price from {website}")
        logs.append(f"Sorry, I couldn't fetch the price from {website}")
        
# Function to get Wikipedia info
def get_wikipedia_info(topic):
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(f"According to Wikipedia: {result}")
    except Exception as e:
        speak(f"Sorry, I couldn't find information about {topic}")

def set_volume(level):
    dRivaces = AudioUtilities.GetSpeakers()
    interface = dRivaces.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    speak(f"Volume set to {level}%")

def adjust_volume(direction):
    dRivaces = AudioUtilities.GetSpeakers()
    interface = dRivaces.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current = volume.GetMasterVolumeLevelScalar() * 100
    if direction == "increase":
        volume.SetMasterVolumeLevelScalar(min(1.0, (current + 20) / 100), None)
    else:
        volume.SetMasterVolumeLevelScalar(max(0.0, (current - 20) / 100), None)
    speak(f"Volume {direction}d")

# Main loop
def run_riva():
    logs = []
    ai_code = None
    speak("Hello, I am Riva your Assistant")
    logs.append("Hello, I am Riva your Assistant")
    speak(f"{get_greeting()} Abhijit Sir")
    logs.append(f"{get_greeting()} Abhijit Sir")
    speak("Say 'Riva' when you need me")
    logs.append("Say 'Riva' when you need me")

    while True:
        listen_for_wake_word()
        while True:
            query = take_command().lower()

            if query == "none" or query.strip() == "":
                speak("I didn't understand that. Please try again.")
                continue  # Keep listening without requiring wake word

            task_completed = False

            if 'create file' in query or 'create folder' in query:
                speak("What name?")
                name = take_command()
                if name == "none":
                    speak("File name not received.")
                    continue
                if 'folder' in query:
                    create_file(name, 'folder')
                else:
                    speak("What type of file?")
                    ftype = take_command()
                    if ftype == "none":
                        speak("File type not received.")
                        continue
                    create_file(name, ftype)
                task_completed = True

            elif 'delete file' in query or 'delete folder' in query:
                speak("Name to delete?")
                delete_file(take_command())
                task_completed = True

            elif 'restore from recycle bin' in query:
                speak("Item name to restore?")
                restore_from_recycle_bin(take_command())
                task_completed = True

            elif 'open' in query:
                app = query.replace('open', '').strip()
                open_application(app)
                task_completed = True

            elif 'time' in query:
                speak(datetime.datetime.now().strftime("%I:%M %p"))
                task_completed = True

            elif 'date' in query:
                speak(datetime.datetime.now().strftime("%B %d, %Y"))
                task_completed = True

            elif 'weather' in query:
                speak("Which city?")
                get_weather(take_command())
                task_completed = True

            elif 'search' in query:
                search_anything(query.replace('search', '').strip())
                task_completed = True

            elif 'play' in query:
                song = query.replace('play', '').replace('music', '').replace('song', '').replace('album', '').replace('by', '').strip()
                play_music(song)
                task_completed = True


            elif 'price' in query:
                if 'amazon' in query:
                    product = query.replace('price on amazon', '').replace('price', '').strip()
                    speak(f"Checking price for {product} on Amazon")
                    get_product_price(product, "amazon")
                elif 'flipkart' in query:
                    product = query.replace('price on flipkart', '').replace('price', '').strip()
                    speak(f"Checking price for {product} on Flipkart")
                    get_product_price(product, "flipkart")
                else:
                    speak("Please specify Amazon or Flipkart for price check")
                task_completed = True

            elif 'volume' in query:
                if 'increase' in query:
                    adjust_volume('increase')
                elif 'decrease' in query:
                    adjust_volume('decrease')
                elif 'set' in query:
                    num = re.findall(r'\d+', query)
                    if num:
                        set_volume(int(num[0]))
                task_completed = True

            elif any(phrase in query for phrase in ['who are you', 'what is your name']):
                speak("I am Riva, your personal desktop assistant.")
                speak("I was developed and trained by Abhijit Adhikari Sir to help you with your everyday tasks.")
                speak("Just say my name and I'm here to assist you.")
                task_completed = True

            elif any(phrase in query for phrase in ['who is abhijit', 'who is abhijeet', 'who is abhijeet adhikari', 'who is abhijit adhikari']):
                speak("Abhijit Adhikari is a passionate developer and creator of mine, Riva.")
                speak("He is skilled in technologies like HTML, CSS, JavaScript, Python, Laravel, and more.")
                speak("He loves building creative and intelligent systems.")
                speak("I'm proud to be developed by him.")
                task_completed = True
                
            elif query.startswith('who is') or query.startswith('what is') or query.startswith('tell me about'):
                topic = query.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
                speak(f"Searching Wikipedia for {topic}")
                get_wikipedia_info(topic)
                task_completed = True
                
            elif query.startswith('who is') or query.startswith('what is') or query.startswith('tell me about'):
                topic = query.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
                speak(f"Searching Wikipedia for {topic}")
                get_wikipedia_info(topic)
                task_completed = True
            
            elif any(cmd in query for cmd in ['create', 'make', 'generate']):
                if any(word in query for word in ['login page', 'calculator', 'form', 'website', 'register', 'api', 'script', 'code']):
                    speak("Working on it, Abhijit Sir. Generating the code...")

                    prompt = f"""
                    You are an expert AI programmer. Return only clean and complete code.

                    TASK: {query}

                    FORMAT RULES:
                    - Return only the code.
                    - Use appropriate language code blocks (like ```html, ```python).
                    - Don't add any explanation, notes, or comments.

                    BEGIN:
                    """

                    ai_response = ask_openrouter(prompt)
                    ai_code = ai_response

                    if not ai_response:
                        speak("I couldn't generate the code. Please try again.")
                        continue

                    speak("Where should I save it? Say something like Downloads, Desktop, or D drive.")
                    location = take_command().lower()

                    extension_map = {
                        "html": ".html", "css": ".css", "javascript": ".js",
                        "python": ".py", "php": ".php", "java": ".java",
                    }

                    ext = ".txt"
                    for key in extension_map:
                        if key in query or key in ai_response.lower():
                            ext = extension_map[key]
                            break

                    folder_map = {
                        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
                        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
                        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
                        "d": "D:/", "d drive": "D:/",
                        "c": "C:/", "c drive": "C:/"
                    }

                    folder = folder_map.get(location, os.path.join(os.path.expanduser("~"), "Desktop"))
                    base_name = query.replace("create", "").replace("make", "").replace("generate", "").strip().replace(" ", "_")
                    filename = f"{base_name}_{datetime.datetime.now().strftime('%H%M%S')}{ext}"
                    full_path = os.path.join(folder, filename)

                    try:
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(ai_response.strip())
                        speak(f"I’ve saved your code as {filename} in {location.title() or 'Desktop'}")
                        os.startfile(full_path)
                    except Exception as e:
                        speak("Oops, something went wrong while saving the file.")
                        print("File Save Error:", e)

                    task_completed = True
                    return logs, ai_code
            
            # Example usage inside your voice query handling logic
            elif any(x in query for x in ["read pdf", "read document", "read file"]):
                speak("Please tell me the file name or folder name.")
                file_hint = take_command().lower()
                status = read_document(file_hint)
                speak(status)
                logs.append(status)


            elif 'exit' in query or 'quit' in query:
                speak("Goodbye Abhijit Sir")
                return  # Exit the main function

            else:
                speak("I didn't understand. Please try again.")
                continue  # Keep listening without wake word

            if task_completed:
                speak("Say 'Riva' again if you need anything else.")
                break  # Go back to waiting for wake word

