from AppOpener import close, open as appopen # To open and close app
from webbrowser import open as webopen # Web functionality
from pywhatkit import search, playonyt # For google search and YouTube playback
from dotenv import dotenv_values
from bs4 import BeautifulSoup # Beautifulsoup for parsing HTML content
from rich import print # For styled console output
from groq import Groq # for AI caht functionalities
import webbrowser # For opening URLs
import subprocess # For interacting with the system
import requests # For making HTTP requests
import keyboard # For keyboard related actions
import asyncio # For asynchronous programming
import os

env_vars = dotenv_values("D:\Python Projects\AI Model\.env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "IZ6rdc", "O5R6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user agent for making web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Intialize the Groq client with thw API key
client = Groq(api_key=GroqAPIKey)

# Predicted professional response for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with."
    "I'm at your service for additional questions or support you may need-don't hesistate to ask"
]

# List to store chatbot messages
messages = []

# Systen message to provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform google search
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Indicate success


# Function to generate content using AI and save it to a file
def Content(Topic):

    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe' # Default text editor
        subprocess.Popen([default_text_editor, File]) # Open the file in Notepad
    
    # Nested function to generate content using the AI chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"(prompt)"}) #Add the user's prompt to messages

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Spicfy the AI model
            messages=SystemChatBot + messages, # Include system instruction and chat histroy
            max_tokens=2048, # Limit the maximum tokens in the response
            temperature=0.7, # Adjust response randomness
            top_p=1, # Use nucleus sampling for response diversity
            stream=True, # Enable streaming response
            stop=None # Allow the model to determine stopping conditions
        )

        Answer = "" # Initialize an empty string for the response

        # Process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content: # Check for content in current chunk
                Answer += chunk.choices[0].delta.content # Append the content to the answer

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from response
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to message
        return Answer
    Topic: str = Topic.replace("Content", "") # Remove content from the topic
    ContentByAI = ContentWriterAI (Topic) # Generate content using AI

    # Save the generated content to a text file
    with open(rf"D:\Python Projects\AI Model\Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8")as file:
        file.write(ContentByAI)
        file.close()

    
    OpenNotepad(rf"D:\Python Projects\AI Model\Data\{Topic.lower().replace(' ', '')}.txt") # Open file in notepad
    return True

# Function to search for topic on YouTube
def PlayYoutube(query):
    playonyt(query) 
    return True

PlayYoutube(Jai shree ram)

# Function to open an application or relevant webpage
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # Attempt to open the app
        return True
    
    except:
          # Extract links from HTML content
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') # Parse the HTML content
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return[link.get('href')for link in links]
        
        # To perform google search and retrive HTML
        def search_google(query):
            url = f"http://www.google.com/search?q={query}" 
            headers = {"User-Agent": useragent} # Use the predefined user-agent
            response = sess.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text  
            else:
                print("Failed to retrieve search results.") # Print an error message
                return None
            
        html = search_google(app) 

        if html:
            link = extract_links(html)[0] # Extract the first link from the search results
            webopen(link)
        return True

# Function to close an application
def CloseApp(app):

    if "chrome" in app:
        pass # Skip if the app is Chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False 
        
# Function to execute system level commands
def System(command):
    def mute():
        keyboard.press_and_release("volume mute") # Simulate the mute key press

    def unmute():
        keyboard.press_and_release("volume unmute") # Simulate the unmute key press

    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the up key press

    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the down key press

    # Execute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    func = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening
                func.append(fun)
        elif command.startswith("general "): 
            pass
        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            func.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            func.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            func.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            func.append(fun)
        
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            func.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            func.append(fun)

        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*func)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass 
    return True