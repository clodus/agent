from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
from ollama import Client

load_dotenv(override=True)
ollama_api_key = os.getenv("OLLAMA_API_KEY")
print(f"OLLAMA_API_KEY: {ollama_api_key}")

if ollama_api_key:
    print(f"OLLAMA_API_KEY is set: {ollama_api_key[:8]}")
else:    
    print(f"OLLAMA_API_KEY is not set.")

#client = Client(
#    host="https://ollama.com",
#    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
#)

client = Client()

messages = [
  {
    'role': 'user',
    'content': 'Trouve moi une egnime',
  },
]
# llama3.2
# gpt-oss:120b

result = ""
for part in client.chat('llama3.2', messages=messages, stream=True):
    chunk = part['message']['content']
    result += chunk


messages = [
  {
    'role': 'user',
    'content': result,
  },
]


for part in client.chat('llama3.2', messages=messages, stream=True):
    print(part['message']['content'], end="", flush=True)