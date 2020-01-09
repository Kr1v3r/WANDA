import speech_recognition as sr  
import playsound 
import random   
from gtts import gTTS   
import os   
import wolframalpha 
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
from io import BytesIO
from io import StringIO
import wikipedia
import smtplib
import datetime
num = 1


def assistant_speaks(output):
    global num
    num +=1
    print("Wanda : ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num)+".mp3"
    toSpeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=5)
    print("Stop.")
    try:
        text = r.recognize_google(audio,language='en-US')
        print("You : ", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, PLease try again!")
        return 0

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        assistant_speaks('Good Morning!')

    if currentH >= 12 and currentH < 18:
        assistant_speaks('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        assistant_speaks('Good Evening!')


def search_web(input):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
    if 'youtube' in input.lower():
        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx+1:]
        driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
        return
    else:
        if 'google' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        elif 'search' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        elif 'email' in query:
            assistant_speaks('Who is the recipient ?')
            recipient = get_audio()

            if 'me' in recipient:
                try:
                    assistant_speaks('What should I say? ')
                    content = get_audio()
        
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", 'Your_Password')
                    server.sendmail('Your_Username', "Recipient_Username", content)
                    server.close()
                    assistant_speaks('Email sent!')

                except:
                    assistant_speaks('Sorry Sir! I am unable to send your message at this moment!')
            
        else:
            driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))
        return


def open_application(input):
    if "chrome" in input:
        assistant_speaks("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return
    elif "firefox" in input or "mozilla" in input:
        assistant_speaks("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\firefox.exe')
        return
    elif "word" in input:
        assistant_speaks("Opening Microsoft Word")
        os.startfile('C:\Program Files (x86)\Microsoft Office\Office15\WINWORD.exe')
        return
    elif "excel" in input:
        assistant_speaks("Opening Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
        return
    elif "Powerpoint" in input:
        assistant_speaks("Opening Powerpoint")
        os.startfile('C:\Program Files (x86)\Microsoft Office\Office15\POWERPNT.exe')
    elif "Outlook" in input:
        assistant_speaks("Opening Outlook")
        os.startfile('C:\Program Files (x86)\Microsoft Office\Office15\OUTLOOK.exe')
        
    elif "My computer" or "File" in input:
        assistant_speaks("Opening File Explorer")
        os.starfile('')
    else:
        assistant_speaks("Application not available")
        return


def process_text(input):
    try:
        if "who are you" in input:
            speak = '''Hello, I am Wanda. Your personal Assistant.
            '''
            assistant_speaks(speak)
            return
        elif "I love you " in input:
            stMsgs=["Awww thats nice but i dont have feelings","Sorry You are just my brother"]
            assistant_speaks(random.choice(stMsgs))
            speak('How are you ?')
            return
        elif "fine" in input:
            speak="oh! good to hear that"
            assistant_speaks(speak)
            return
        elif "who made you" in input or "who is your father" in input :
            speak="Oh i was created simply as a wikipedia bot. which then extended to a personal assistant"
            assistant_speaks(speak)
            return
        elif "crazy" in input:
            speak = """Am I ?"""
            assistant_speaks(speak)
            return
        elif "time" in input :
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            assistant_speaks(f"the time is {strTime}")
            return
        elif "wikipedia" in input :
            results = wikipedia.summary(input.lower(), sentences=2)
            assistant_speaks('Got it.')
            assistant_speaks('According to wikipedia : ')
            assistant_speaks(results)
            return  
        elif "calculate" in input.lower():
            app_id= "E46YXW-T5LG6RT7K7"
            client = wolframalpha.Client(app_id)

            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assistant_speaks("The answer is " + answer)
            return
        elif 'open' in input:
            open_application(input.lower())
            return
        elif 'search' in input or 'play' in input:
            search_web(input.lower())
            return
        else:
            assistant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else:
                return
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)


if __name__ == "__main__":
    greetMe()
    assistant_speaks("What's your name , Boss")
    name ='Boss'
    name=get_audio()
    assistant_speaks("Hello, " + name + '.')
    assistant_speaks("What can i do for you?")
    while(1):
        text = get_audio().lower()
        if text == 0:
            continue
        #assistant_speaks(text)
        if "exit" in str(text) or "bye" in str(text) or "go " in str(text) or "sleep" in str(text) or "good bye" in str(text):
            assistant_speaks("Ok bye, "+ name+'.')
            break
        process_text(text)
