from groq.types import model
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ConfigDict

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key kaha hai")



client = Groq(api_key=my_api_key)
model ="openai/gpt-oss-120b"
role="user"
class Ticket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    email: str
    issue: str
    address: str
    contact_number: str
    product: str
schema=Ticket.model_json_schema()    
response_format= {
    "type": "json_schema",
    "json_schema": {
        "name": "customer_ticket",
        "strict": True,
        "schema": schema
    }
}
system_prompt =f"""extract the personal information from this ticket strictly based on this schema {schema} and give me information in the json format """
message_system={
    "role":"system",
    "content":system_prompt
}
    
                 

       
text="my name is mayank i have ordered mac air m2 and it is not working and my address is vidisha email id is hello@gmail.com and contact number is 87700"

prompt= f"""this is a customer query please extract the personal information from this {text} """
message={
    "role":role,
    "content":prompt

}
messages = [message_system,message]
response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=response.choices[0].message.content
print(answer)
# print(response)

# how the computer will read it and use it
import json
raw_json = answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)
# ticket=Ticket(
#     name=data_file["name"],
#     email=data_file["email"],
#     issue=data_file["issue"]
# )
print(ticket)
print(type(ticket))


    