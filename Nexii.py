"""speechrecognition
   pyaudio
   setuptools 
   webbrowser  -- is build in module
   pyttsx3    -- text to speech
   pocketsphinx
   requests
    """
import speech_recognition  as sr  
import webbrowser   
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai
import os

Geminiapi = os.getenv("Geminiapi") 
newsapi = os.getenv("Newsapi")

 
# Configure Google Gemini API
genai.configure(api_key=Geminiapi)

model = genai.GenerativeModel("gemini-pro")

#speech
recognizer = sr.Recognizer()  #recognizier is a class
engine = pyttsx3.init()

#voice rate  fast or slow
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 190)

#voice female ; 0 for male
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def aiProcess(command):
    response = model.generate_content(command)
    return " ".join(response.text.split()[:300])  

    
def processCommand(c):
    print(f'You say "{c}"')
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the music library.")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=technology&language=en&pageSize=10&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        finOutput = output.replace("*",".")
        print(finOutput)
        speak(finOutput)  
    
if __name__ == "__main__":
    print("\n\n--------------Your Assistant NEXI Welcomes you-----------------\n\n")
    speak("Hello I am your assistant Nexi....")

    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("....Listening....")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print(word)
            if(word.lower() == "nexi"):
                speak("Yahhh say. What can i help you?")
                # Listen for command
                with sr.Microphone() as source:
                    print("****Nexi Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)
            
            elif(word.lower() == "exit"):
                speak("Bye Bye. Have a nice day")
                break

        except Exception as e:
            print(f"\nError: {e}\n")
        