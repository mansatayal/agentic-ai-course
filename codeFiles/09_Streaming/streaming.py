import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key is missing")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"

prompt = "explain how internet works"
message = {"role" : "user" , "content" : prompt}

messages = [message]


# without streaming:
# response = client.chat.completions.create(model = model, messages = messages)
# answer = response.choices[0].message.content
# print(answer)


# with streamin:
#by default streming is false
stream = client.chat.completions.create(model = model, messages = messages, stream = True)  

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end = "", flush = True)      #flush = true print immediately 