from openai import OpenAI; from dotenv import load_dotenv; import os
load_dotenv(); client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("ChatGPT with Memory. Type 'quit' to exit.\n")

while True:
    userInput = input("You: ")

    if userInput.lower() == "quit":
        break
    messages.append({"role": "user", "content": userInput})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = messages
    )
    aiMessage = response.choices[0].message.content
    messages.append({"role": "assistant", "content": aiMessage})
    print(f"AI: {aiMessage}\n")
