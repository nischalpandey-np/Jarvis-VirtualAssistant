
import speech_recognition as sr  # Recognizes voice
import webbrowser 
import pyttsx3  # Text to speech
import musicLibrary  # Assuming you have a custom library for music
import requests  # For making HTTP requests


# Initialize speech recognition and text to speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


newsapi = 'your api here'


def jarvisCommand(command):
    """
    Processes various commands given to Jarvis.
    """
    if 'open gmail' in command.lower():
        webbrowser.open("https://mail.google.com/mail")
        textToSpeech("Opening Gmail")
    elif 'open youtube' in command.lower():
        webbrowser.open("https://youtube.com")
        textToSpeech("Opening YouTube")
    elif 'open facebook' in command.lower():
        webbrowser.open("https://facebook.com")
        textToSpeech("Opening Facebook")
    elif 'open chatgpt' in command.lower():
        webbrowser.open("https://chatgpt.com/?model=auto")
        textToSpeech("Opening ChatGPT")
    elif 'open messenger' in command.lower():
        webbrowser.open("https://messenger.com")
        textToSpeech("Opening Messenger")
    elif command.lower().startswith("play"):
        # Assuming 'play' is followed by a song name
        song = command.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            textToSpeech(f"Sorry, {song} is not available in the library.")
    
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                print(article['title'])
                textToSpeech(article['title'])

def textToSpeech(text):
    """
    Uses text-to-speech engine to speak the given text.
    """
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    print('Initializing Jarvis...')
    textToSpeech("Initializing Jarvis...")

    while True:
        # Listen for the wake word "Jarvis"
        r=sr.Recognizer()
        print("Listening...")

        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            
            if word.lower() == "jarvis":
                print("Jarvis Activated!")
                textToSpeech("Jarvis Activated!")
                
                # Listen for command after wake word
                try:
                    with sr.Microphone() as source:
                        textToSpeech("Listening...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        jarvisCommand(command)
                except sr.UnknownValueError:
                    textToSpeech("Sorry, could not understand the command")
                except sr.RequestError:
                    textToSpeech("Sorry, could not connect to Google Speech Recognition")
        
        except sr.WaitTimeoutError:
            print("Timeout!!")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Could not request results")
