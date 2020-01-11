import speech_recognition as sr  #for voice recogonition
import playsound #to play the audio
import random   #to make random choices
from gtts import gTTS  #google text to speech package 
import os  #to manage the files 
import wolframalpha #a computational knowledge engine
import webbrowser #to manage browser
import wikipedia #to Get Wikipeda information
import smtplib #To sent email
import datetime #for date and time
import sys #to manipulate the different parts of the python environment
num = 1


def assistant_speaks(output): #output audio and text 
    global num
    num +=1
    print("Wanda : ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num)+".mp3"
    toSpeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)
def get_audio(): #to get input audio and convert it into text 
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


def send_mail(input):   #funtion to send mail
    if 'email' in input :
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
            webbrowser.open('www.google.com')
        return
def search_web(input): #to open google for search
    webbrowser.open('www.google.com')
    return

def open_application(input): #open applications and browser
    if "chrome" in input:
        assistant_speaks("Chrome")
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
    elif 'youtube' in input:
        assistant_speaks('okay') 
        webbrowser.open('www.youtube.com')
    elif 'google' in input :
        assistant_speaks('okay')
        webbrowser.open('www.google.co.in')

    elif 'gmail' in input :
        assistant_speaks('okay')
        webbrowser.open('www.gmail.com')
    else:
        assistant_speaks("Application not available")
        return


def process_text(input): #function to interact with assistant and also to determine other functions
    try:
        if "who are you" in input:
            speak = '''Hello, I am Wanda. Your personal Assistant'''
            assistant_speaks(speak)
            return
        elif "i love you" in input:
            stMsgs=['that was nice but i dont have feelings','Sorry You are just my brother']
            assistant_speaks(random.choice(stMsgs))
            return
        elif "what's up" in input or 'how are you' in input:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            assistant_speaks(random.choice(stMsgs))
            assistant_speaks('How are you ?')
            return
        elif "fine" in input:
            speak="oh! good to hear that"
            assistant_speaks(speak)
            return
        elif "who made you"  in input :
            speak="Oh i was created simply as a wikipedia bot. which then extended to a personal assistant"
            assistant_speaks(speak)
            return
        elif 'hello' in input or 'hey' in input or 'hi' in input:
            stMsgs = ['Hello', 'hip hip . hey', 'whats up', 'hi']
            assistant_speaks(random.choice(stMsgs))
            return
        elif "crazy" in input:
            speak = """Am I ? Okay"""
            assistant_speaks(speak)
            return
        elif "joke" in input :
            stMsgs=["I just got a photo from a speeding camera through the mail. I send it right back - way too expensive and really bad quality","8 pm I get an SMS from my girlfriend : Me or football?! 11pm. I SMS my girlfriend.You ofcourse."]
            assistant_speaks(random.choice(stMsgs))
            return
        elif "thanks" in input or "thank you" in input:
            stMsgs=["Its okay","just doing my thing","You'r welcome"]
            assistant_speaks(random.choice(stMsgs))
            return
        elif "time" in input :
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            assistant_speaks(f"the time is {strTime}")
            return
        elif 'bye' in input:
            currentH = int(datetime.datetime.now().hour)
            if currentH >= 18 and currentH !=0:
                speak('Good Night')
            else:
                stMsgs=['Bye , have a good day.','see you soon']
                speak(random.choice(stMsgs))
                sys.exit()      
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
        elif 'send mail' in input :
            send_mail(input.lower())
        else :
            query = input
            assistant_speaks('Let me see')
            try:
                try:
                    client = wolframalpha.Client('XVLP9Q-7YTYAQ3WHA')
                    res = client.query(query)
                    results = next(res.results).text
                    assistant_speaks('Got it.')
                    assistant_speaks(results)
                except:
                    assistant_speaks("I can search the web for you, Do you want to continue?")
                    ans = get_audio()
                    if 'yes' in str(ans) or 'yeah' in str(ans):
                        search_web(input)
            except :
                return
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)


if __name__ == "__main__": #to run directly 
    greetMe()
    assistant_speaks("What's your name , Boss")
    name=get_audio()
    assistant_speaks("Hello, " + name + '.')
    assistant_speaks("What can i do for you?")
    while(1):
        text = get_audio().lower()
        if text == 0:
            continue
        if "exit" in str(text) or "bye" in str(text) or "good bye" in str(text):
            assistant_speaks("see you soon, "+ name +'.')
            break
        process_text(text)
