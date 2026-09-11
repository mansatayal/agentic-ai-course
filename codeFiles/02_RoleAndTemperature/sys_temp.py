import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api error")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"
role = "user"
prompt = "suggest a name for my food company"

# system role
message_system={
    "role" : "system",
    "content" : "you're a brand manager who suggests name for my food company. name should be in one word. suggest one name only"
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]

# temperature by default is 0 meaning safe    (in groq you can set 0, 1 , 2   2 is risky)
response = client.chat.completions.create(model = model, messages = messages, temperature = 2)

answer = response.choices[0].message.content
print(answer)