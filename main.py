import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from google import genai

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "6deeb970bf87448f93d6b0134318b529"


def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = genai.Client(api_key="AIzaSyBd_TXafzL48KcpMn8N8nf14vJJ7rmf6og")
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=command
    )
    return(response.text)
    


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song =  c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=6deeb970bf87448f93d6b0134318b529")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        #let openAI handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initialising Jarvis....")

    #Listen for the wake word jarvis
    while True:
        r = sr.Recognizer()
        
        print("recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                
                audio = r.listen(source, timeout=2, phrase_time_limit=1)        

            word = recognizer.recognize_google(audio, language="en-IN")
            if(word.lower() == "jarvis"):
                speak("Yes")

                #listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
