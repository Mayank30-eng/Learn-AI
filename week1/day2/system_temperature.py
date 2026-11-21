from groq.types import model
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key kaha hai")



client = Groq(api_key=my_api_key)
model ="openai/gpt-oss-120b"
role="user"
# prompt="I love U baby"
prompt="suggest a name for my food company"


message_system={
    "role":"system",
    "content":"you are a brand manager who suggests names for companies and the name shoud be in the one word "
    # "content":"You are my strict office collegue and my senior manager"

    # "content":"You are my loving girlfriend"
    # "content":"You are a very rude person and you always hate people"
}
message={
    "role":role,
    "content":prompt

}
# The model receives both messages as context.
messages = [message_system,message]
response= client.chat.completions.create(model=model,messages=messages,temperature=2)
print(response.choices[0].message.content)
# print(response)


    