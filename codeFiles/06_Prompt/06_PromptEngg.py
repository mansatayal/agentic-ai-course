import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api jey absent")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"


def llm_ans(prompt):
    message = {
        "role" : "user",
        "content" : prompt
    }

    messages = [message]

    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer

bad_prompt = """
this is a user complaint:
1. My laptop is not working.
2. MY girlfriend left me. 
classify this
"""

good_prompt = """
Role:
You're a support assistant at a mobile laptop company

task:
you have to classify the issue in a category

constraint:
you've to classify the issue in the one of the three categories namely billing, technical, return

output format:
your answer should be in one word only. the one word should be one of the categories given in constraints

example:
for instance if a user complaint says refund category is return

fallback: 
if the issue is unrelated to any of the categories mentioned in constraints, then the answer should be OTHER

this is a user complaint:
1. My laptop is not working.
2. MY girlfriend left me. 
"""

print("bad-------------------------------------------\n", llm_ans(bad_prompt))
print("good-------------------------------------------\n", llm_ans(good_prompt))
