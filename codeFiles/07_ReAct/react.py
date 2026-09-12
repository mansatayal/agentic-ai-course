import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep
import re

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key is absent")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"


# tools:    (here we're making tools but in reality we call api)

def get_product_price(product):
    if product == "iPhone 17":
        return 2000
    elif product == "iPhone 15":
        return 1000
    else:
        return 0


def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"


tools = {
    "get_product_price" : get_product_price,
    "calculator" : calculator
}


system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):
    messages = [
        {    
            "role" : "system",
            "content" : system_prompt
        },
        {
            "role" : "user",
            "content" : question
        }
    ]


    # here we're assuming that the task would be done in 5 steps/ tools can be rewritten as per the need
    for step in range(5):
        print("\n-------------------------------------")
        print("STEP ", step + 1)
        print("---------------------------------------")

        response = client.chat.completions.create(model = model, messages = messages, temperature = 0,stop=["\nObservation:", "\nObservation :"])
        answer = response.choices[0].message.content
        print(answer)

        # because we've written in the format that we need a final answer it'll check it to break the function
        if "Final Answer" in answer:
            break;        


        # find the action
        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",    #regular expression
            answer,
            re.IGNORECASE
        )

        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)
            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"')

            # run the tool:
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = "Tool not found"

            print("obsevation: ", observation)


            # add llm response to memory:
            messages.append(
                {
                    "role" : "assistant",
                    "content" : answer
                }
            )

            # give tool result back to llm
            messages.append({
                "role" : "user",
                "content" : "observation: " + str(observation)      # appending observation so the llm remembers the price of iphone before calling calculator
            })
            sleep(5)



prompt = """
what is the price of an iPhone17? I've 8000 rupees. how much money will i be left with?
"""

run_agent(prompt)