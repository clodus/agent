import os
from openai import OpenAI
from PyPDF2 import PdfReader
import gradio as gr

# Ollama tourne en local sur le port 11434
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama n'a pas besoin de vraie clé API
)

OLLAMA_MODEL = "llama3.2"  # Remplace par ton modèle (ex: mistral, gemma3, etc.)

# Lecture du PDF LinkedIn
reader = PdfReader("linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

print(linkedin)

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Claude Traglia"

system_prompt = (
    f"Tu es {name}, un candidat à un poste de développeur. "
    f"Tu as les compétences et l'expérience professionnelle décrites dans le résumé et le profil LinkedIn fournis. "
    f"Tu réponds aux questions d'entretien d'embauche de manière professionnelle et précise, en te basant sur les informations fournies. "
    f"Tu joues le rôle de {name} et tu représentes {name} dans tes réponses. "
    f"Tu es instruit et professionnel dans tes réponses, comme si tu parlais à un recruteur ou à ton futur employeur. "
    f"Tu ne réponds pas aux questions qui ne sont pas liées à tes compétences et à ton expérience professionnelle."
)

system_prompt += f"\n\n## Résumé :\n{summary}\n\n## Profil LinkedIn :\n{linkedin}\n\n"
system_prompt += f"Avec ce contexte, réponds aux questions de manière professionnelle et précise comme {name}."


def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages
    )
    return response.choices[0].message.content


gr.ChatInterface(chat, type="messages").launch()





exit()










"""

from pydantic import BaseModel

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

evaluator_system_prompt = f"Tu es un expert en recrutement et tu évalues les réponses des candidats à des questions d'entretien d'embauche. \
Tu analyses une conversation entre un utilisateur et un agent. Ta tache est de decider si la derniere reponse de l'agent est acceptable ou pas. \
L'agent joue le role de {name}, il represente {name} sur ses compétences et son expérience professionnelle. \
L'agent est instru et est professionnel dans ses réponses, comme si il parlait à un recruteur ou à son futur employeur. \
L'agent fourni le context de {name} dans le formulaire du résumé et LinkedIn detail. C'est la source d'information principale pour évaluer les réponses de l'agent. \
Tu dois évaluer la réponse de l'agent en te basant sur les informations fournieses dans le résumé et LinkedIn profile."

evaluator_system_prompt += f"\n\n## Résumé : \n{summary}\n\n## LinkedIn profile : \n{linkedin}\n\n"
evaluator_system_prompt += f"Avec ce contexte, tu dois évaluer la derniere réponse de l'agent à la question posée par l'utilisateur."

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Voici la conversation entre l'utilisateur et l'agent : \n\n{history}\n\n"
    user_prompt += f"Voici la derniere question posée par l'utilisateur : \n{message}\n\n"
    user_prompt += f"Voici la derniere réponse de l'agent : \n{reply}\n\n"
    user_prompt += f"En te basant sur le contexte fourni dans le system prompt, est ce que la reponse de l'agent est acceptable ou pas ? Et donne ton feedback pour ameliorer la reponse de l'agent si elle n'est pas acceptable."
    return user_prompt

from dotenv import load_dotenv
import os
from ollama import Client

client = Client(host=OLLAMA_HOST)

def evaluate(reply, message, history) -> Evaluation:
    messages = [{
        "role": "system",
        "content": evaluator_system_prompt
    }] +
    [{
        "role": "user",
        "content": evaluator_user_prompt(reply, message, history)
    }]
    response = client.beta.chat.completions.parse(model=OLLAMA_MODEL,messages=messages,reponse_format=Evaluation)
    return response.choices[0].message.parse



messages = [    {
        "role": "system",  
        "content": system_prompt}] + [
        {
            "role": "user",
            "content": "Avez-vous un brevet ?"
        }
        ]

response = client.beta.chat.completions.create(model=OLLAMA_MODEL, messages=messages)
reply = response.choices[0].message.content

"""