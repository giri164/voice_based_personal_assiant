import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import random
import time
import threading
import subprocess
import json
import re
from pathlib import Path

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configuration file for API keys and settings
CONFIG_FILE = "jarvis_config.json"

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "openweather_api_key": "YOUR_OPENWEATHERMAP_API_KEY",
        "news_api_key": "YOUR_NEWSAPI_API_KEY",
        "notes_file": "jarvis_notes.txt",
        "reminders_file": "jarvis_reminders.json"
    }

# Save configuration
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

# Global variables for reminders and timers
active_reminders = []
active_timers = []

# Function to speak text
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen for commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Could not request results; check your network connection.")
            return None

# Function to perform Google search
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}.")

# Function to get weather information
def get_weather(city):
    api_key = config.get("openweather_api_key", "YOUR_OPENWEATHERMAP_API_KEY")
    if api_key == "YOUR_OPENWEATHERMAP_API_KEY":
        speak("Please set your OpenWeatherMap API key in the configuration file.")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url, timeout=10)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]
            wind_speed = data["wind"]["speed"]
            speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}. Humidity is {humidity} percent, and wind speed is {wind_speed} meters per second.")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Unable to retrieve weather information. Please check your internet connection.")

# Function to set reminders
def set_reminder(reminder_time, message):
    try:
        # Parse time (simple parsing for minutes)
        if "minute" in reminder_time or "minutes" in reminder_time:
            minutes = int(re.findall(r'\d+', reminder_time)[0])
            delay = minutes * 60
        elif "hour" in reminder_time or "hours" in reminder_time:
            hours = int(re.findall(r'\d+', reminder_time)[0])
            delay = hours * 3600
        else:
            speak("Please specify time in minutes or hours.")
            return

        speak(f"Reminder set for {reminder_time}.")
        reminder_thread = threading.Timer(delay, lambda: speak(f"Reminder: {message}"))
        reminder_thread.start()
        active_reminders.append(reminder_thread)
    except Exception as e:
        speak("Sorry, I couldn't set that reminder. Please try again.")

# Function to set a timer
def set_timer(duration, message="Time's up!"):
    try:
        if "minute" in duration or "minutes" in duration:
            minutes = int(re.findall(r'\d+', duration)[0])
            delay = minutes * 60
        elif "second" in duration or "seconds" in duration:
            seconds = int(re.findall(r'\d+', duration)[0])
            delay = seconds
        else:
            speak("Please specify duration in minutes or seconds.")
            return

        speak(f"Timer set for {duration}.")
        timer_thread = threading.Timer(delay, lambda: speak(message))
        timer_thread.start()
        active_timers.append(timer_thread)
    except Exception as e:
        speak("Sorry, I couldn't set that timer. Please try again.")

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and now it won't stop sending me KitKat ads.",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the bicycle fall over? It was two-tired.",
        "What do you call a fish wearing a bowtie? Sofishticated.",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one."
    ]
    joke = random.choice(jokes)
    speak(joke)

# Function to provide help
def provide_help():
    speak("Here are some things I can do:")
    speak("Time and date: 'what time is it', 'what's the date'")
    speak("Weather: 'weather in [city]'")
    speak("Reminders: 'remind me in 5 minutes to [message]'")
    speak("Timer: 'set timer for 10 minutes'")
    speak("Jokes: 'tell me a joke'")
    speak("News: 'get news' or 'news'")
    speak("Calculations: 'calculate 2 + 2' or 'math 5 * 3'")
    speak("Notes: 'take a note [text]' or 'read notes'")
    speak("Open apps: 'open calculator', 'open chrome', 'open word'")
    speak("System control: 'shutdown', 'restart', 'lock computer', 'sleep'")
    speak("Search: 'search google for [query]' or 'search files for [filename]'")
    speak("System info: 'system info'")
    speak("Say 'exit' or 'bye' to quit.")

# Function to get news updates
def get_news():
    api_key = config.get("news_api_key", "YOUR_NEWSAPI_API_KEY")
    if api_key == "YOUR_NEWSAPI_API_KEY":
        speak("Please set your News API key in the configuration file.")
        return

    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            articles = response.json()["articles"]
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles[:5], 1):  # Get top 5 articles
                speak(f"{i}. {article['title']}")
        else:
            speak("Failed to retrieve news. Please check your API key.")
    except Exception as e:
        speak("Unable to retrieve news. Please check your internet connection.")

# Function to perform calculations
def calculate(expression):
    try:
        # Remove potentially dangerous functions
        safe_dict = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'len': len, 'pow': pow, 'sqrt': lambda x: x**0.5
        }
        result = eval(expression, {"__builtins__": None}, safe_dict)
        speak(f"The result is {result}.")
    except Exception as e:
        speak("Sorry, I couldn't calculate that. Please check your expression.")

# Function to take notes
def take_note(note):
    notes_file = config.get("notes_file", "jarvis_notes.txt")
    try:
        with open(notes_file, 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {note}\n")
        speak("Note saved.")
    except Exception as e:
        speak("Sorry, I couldn't save the note.")

# Function to read notes
def read_notes():
    notes_file = config.get("notes_file", "jarvis_notes.txt")
    try:
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as f:
                notes = f.read()
            if notes.strip():
                speak("Here are your notes:")
                speak(notes)
            else:
                speak("You have no notes.")
        else:
            speak("You have no notes.")
    except Exception as e:
        speak("Sorry, I couldn't read your notes.")

# Function to open files or applications
def open_file_or_app(name):
    try:
        if name.lower() in ["chrome", "google chrome"]:
            subprocess.run(["start", "chrome"], shell=True)
            speak("Opening Google Chrome.")
        elif name.lower() in ["firefox"]:
            subprocess.run(["start", "firefox"], shell=True)
            speak("Opening Firefox.")
        elif name.lower() in ["word", "microsoft word"]:
            subprocess.run(["start", "winword"], shell=True)
            speak("Opening Microsoft Word.")
        elif name.lower() in ["excel", "microsoft excel"]:
            subprocess.run(["start", "excel"], shell=True)
            speak("Opening Microsoft Excel.")
        elif name.lower() in ["powerpoint", "microsoft powerpoint"]:
            subprocess.run(["start", "powerpnt"], shell=True)
            speak("Opening Microsoft PowerPoint.")
        elif name.lower() in ["calculator"]:
            subprocess.run(["calc"])
            speak("Opening Calculator.")
        elif name.lower() in ["file explorer", "explorer"]:
            subprocess.run(["explorer"])
            speak("Opening File Explorer.")
        else:
            # Try to open as a file
            if os.path.exists(name):
                os.startfile(name)
                speak(f"Opening {name}.")
            else:
                speak(f"I don't know how to open {name}.")
    except Exception as e:
        speak(f"Sorry, I couldn't open {name}.")

# Function to perform system control
def system_control(action):
    try:
        if action == "shutdown":
            speak("Shutting down the system in 30 seconds. Say 'cancel shutdown' to abort.")
            os.system("shutdown /s /t 30")
        elif action == "restart":
            speak("Restarting the system in 30 seconds. Say 'cancel restart' to abort.")
            os.system("shutdown /r /t 30")
        elif action == "cancel shutdown" or action == "cancel restart":
            os.system("shutdown /a")
            speak("Shutdown cancelled.")
        elif action == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            speak("Locking the computer.")
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            speak("Putting the computer to sleep.")
        else:
            speak("I don't recognize that system command.")
    except Exception as e:
        speak("Sorry, I couldn't perform that system action.")

# Function to search files
def search_files(query):
    try:
        result = subprocess.run(["dir", "/s", f"*{query}*"], capture_output=True, text=True, shell=True)
        if result.stdout:
            speak("Found the following files:")
            speak(result.stdout[:500])  # Limit output
        else:
            speak("No files found matching that query.")
    except Exception as e:
        speak("Sorry, I couldn't search for files.")

# Function to get system information
def get_system_info():
    try:
        import platform
        system = platform.system()
        release = platform.release()
        version = platform.version()
        speak(f"You are running {system} {release}, version {version}.")
    except Exception as e:
        speak("Sorry, I couldn't get system information.")

# Function to execute commands
def execute_command(command):
    if "hello" in command or "hi" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}.")
    elif "open" in command:
        if "browser" in command or "google" in command:
            webbrowser.open("http://www.google.com")
            speak("Opening the web browser.")
        elif "notepad" in command:
            os.system("notepad")
            speak("Opening Notepad.")
        elif "spotify" in command:
            webbrowser.open("https://open.spotify.com")
            speak("Opening Spotify.")
        elif "youtube" in command:
            webbrowser.open("http://www.youtube.com")
            speak("Opening YouTube.")
        elif "calculator" in command:
            open_file_or_app("calculator")
        elif "file explorer" in command or "explorer" in command:
            open_file_or_app("file explorer")
        else:
            # Extract app/file name from command
            app_name = command.replace("open", "").strip()
            open_file_or_app(app_name)
    elif "weather" in command:
        city = command.replace("weather in", "").replace("weather", "").strip()
        if city:
            get_weather(city)
        else:
            speak("Please specify a city for weather information.")
    elif "remind me" in command or "reminder" in command:
        # Parse reminder command
        parts = command.split("to")
        if len(parts) > 1:
            time_part = parts[0].replace("remind me", "").replace("reminder", "").strip()
            message = parts[1].strip()
            set_reminder(time_part, message)
        else:
            speak("Please specify when to remind you and what to remind you about.")
    elif "set timer" in command or "timer" in command:
        duration = command.replace("set timer for", "").replace("timer for", "").replace("set timer", "").replace("timer", "").strip()
        if duration:
            set_timer(duration)
        else:
            speak("Please specify the timer duration.")
    elif "tell me a joke" in command or "joke" in command:
        tell_joke()
    elif "news" in command:
        get_news()
    elif "calculate" in command or "math" in command:
        expression = command.replace("calculate", "").replace("math", "").strip()
        if expression:
            calculate(expression)
        else:
            speak("Please provide an expression to calculate.")
    elif "note" in command or "remember" in command:
        if "read" in command or "show" in command:
            read_notes()
        else:
            note_text = command.replace("take a note", "").replace("note", "").replace("remember", "").strip()
            if note_text:
                take_note(note_text)
            else:
                speak("What would you like me to note?")
    elif "search" in command:
        if "google" in command or "web" in command:
            query = command.replace("search google for", "").replace("google search", "").replace("search web for", "").strip()
            if query:
                google_search(query)
            else:
                speak("What would you like to search for?")
        elif "files" in command or "file" in command:
            query = command.replace("search files for", "").replace("search file for", "").strip()
            if query:
                search_files(query)
            else:
                speak("What file would you like to search for?")
    elif "system" in command:
        if "info" in command:
            get_system_info()
        elif "shutdown" in command:
            system_control("shutdown")
        elif "restart" in command:
            system_control("restart")
        elif "cancel shutdown" in command or "cancel restart" in command:
            system_control("cancel shutdown")
        elif "lock" in command:
            system_control("lock")
        elif "sleep" in command:
            system_control("sleep")
        else:
            speak("What system action would you like to perform?")
    elif "help" in command or "what can you do" in command:
        provide_help()
    elif "exit" in command or "quit" in command or "bye" in command:
        speak("Goodbye!")
        return False
    else:
        # Try to interpret as a general search
        if len(command.split()) > 2:
            google_search(command)
        else:
            speak("I'm not sure how to help with that. Try saying 'help' for available commands.")
    return True
# Main loop
def main():
    speak("Hello! I am Jarvis, your personal assistant. Say 'help' to see what I can do.")
    try:
        while True:
            command = listen()
            if command:
                if not execute_command(command):
                    break
    except KeyboardInterrupt:
        speak("Goodbye!")
    finally:
        # Clean up any active reminders and timers
        for reminder in active_reminders:
            if reminder.is_alive():
                reminder.cancel()
        for timer in active_timers:
            if timer.is_alive():
                timer.cancel()
        speak("All reminders and timers cancelled. Shutting down.")

if __name__ == "__main__":
    main()