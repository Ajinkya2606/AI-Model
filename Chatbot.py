from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

#Load envir var from .env file
env_vars = dotenv_values("D:\Python Projects\AI Model\.env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

# Inatialize an empty list to store chat messages.
message = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instruction for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file.
try:
    with open(r"D:\Python Projects\AI Model\Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    # Create a new JSON file 
    with open(r"D:\Python Projects\AI Model\Data\ChatLog.json", "w") as f:
        dump([], f)

# Real Date and Time Information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A") # week
    date = current_date_time.strftime("%d") # month
    month = current_date_time.strftime("%B") # month name
    year = current_date_time.strftime("%Y") # Year
    hour = current_date_time.strftime("%H") # 24 hours format
    minute= current_date_time.strftime("%M") # minute
    second = current_date_time.strftime("%S") # second

    # into string
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

# Modify Chatbot response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()] # remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Handle user queries
def ChatBot(Query):
    """ This function sends the user query to the chatbot and returns the AI's response. """

    try:
        with open(r"D:\Python Projects\AI Model\Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Append the user's query to message list
        messages.append({"role": "user", "content": f"{Query}"})

        # request to Groq API response
        completion = client.chat.completions.create(
            model="llama3-70b-8192", 
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = "" #Initialize an empty string to store the AI's response

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content #Append the content to the answer

        Answer = Answer.replace("<\s>", "")

        messages.append({"role": "assistant", "content": Answer})

        # save updated file 
        with open(r"D:\Python Projects\AI Model\Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:
        print(f"Error: {e}")
        with open(r"D:\Python Projects\AI Model\Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)
# Main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))