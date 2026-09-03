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

from pydantic import BaseModel

# format
class Ticket(BaseModel):
    name : str
    email: str
    phone: int
    issue: str

schema = Ticket.model_json_schema()

response_format = {
    "type" : "json_object"
}


# system role
system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema and give me a json output.
{schema}
"""     #writing json here is compulsory else an error will be there

message_system = {
    "role" : "system",
    "content" : system_prompt
}


# input 
text = "My name is Mansa. I bought a phone from your website which isn't working now. My address is of delhi. Please resolve my problem as soo as possible. you can contact me at mansa@gmail.com or 7848345000."


# user role
prompt = f"""
This is a customer ticket. Please extract the personal information and issue from this. {text}
"""

message = {
    "role" : "user",
    "content" : prompt
}

messages = [message_system ,message]

response = client.chat.completions.create(model = model, messages = messages, response_format = response_format , temperature = 1)

answer = response.choices[0].message.content
print(answer)


# how to read a json file:
import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.phone)
print(ticket.issue)
print(ticket.email)

