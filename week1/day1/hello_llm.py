from groq.types import model
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
# This is called input/configuration validation.
if not my_api_key:
    raise ValueError("API key kaha hai")



client = Groq(api_key=my_api_key)
model ="openai/gpt-oss-120b"
role="user"
prompt= input("What do you want to ask? ")
message={
    "role":role,
    "content":prompt

}
messages = [message]
response= client.chat.completions.create(model=model,messages=messages,stream=True)
for chunk in response:
    content=chunk.choices[0].delta.content

    if content:
        print(content,end="",flush=True)

# print(response.choices[0].message.content)
# # print(response)


    