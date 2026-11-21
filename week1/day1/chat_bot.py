
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"

# Conversation history
messages = []

while True:

    prompt = input("You: ")

    if prompt.lower() == "exit":
        print("Chat ended!")
        break
    if prompt.lower() == "clear":
      messages.clear()
      print("Chat history cleared!")
      continue
    # Store user message
    messages.append({
        "role": "user",
        "content": prompt
    })

    # Send conversation history
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        top_p=0.9,
        stream=True
    )

    # Extract AI response with streaming
    print("AI: ", end="", flush=True)
    full_answer = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_answer += content
    print()

    # Store AI response
    messages.append({
        "role": "assistant",
        "content": full_answer
    })
