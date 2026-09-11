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

prompt1 = "Hi!"
prompt2 = "Exaplain time travel in detail in 100 words"
prompt3 = "Write a 1000 word essay on machine learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
        "role" : role,
        "content" : prompt
    }

    messages = [message]

    response = client.chat.completions.create(model = model, messages = messages, max_tokens = 77)
    usage = response.usage

    # finish reason :               stop naturally was under the token limit
    # finish reason: length         you forcefully vut it in between 
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens} cpmpleteion tokens: {usage.completion_tokens} total tokens: {usage.total_tokens}  Finish Reason: {response.choices[0].finish_reason}")

    answer = response.choices[0].message.content
    print(answer)





