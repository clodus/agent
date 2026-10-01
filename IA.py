####################################################################################################
# PARTIE 1
####################################################################################################

from dotenv import load_dotenv
load_dotenv(override=True)
import os
import json

#########################
#########################

# LLM providers
from openai import OpenAI

# INSTANCE
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = os.getenv("GOOGLE_API_KEY")
gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)

#########################
#########################
# List MESSAGE
messages = [{"role": "user", "content": "What is 2+2?"}]

# CHOOSE MODEL
model = "gemini-2.5-flash-preview-05-20"

# FIRST CALL
response = gemini.chat.completions.create(
    model=model,
    messages=messages
)

result = response.choices[0].message.content

# SECOND CALL
messages = [{"role": "user", "content": f"Present a pain-point in that {result} industry..."}]

response = gemini.chat.completions.create(
    model=model,
    messages=messages
)

pain_point = response.choices[0].message.content
#########################
#########################


##################################################
# PATTERN COMPETITOR 
##################################################
openai = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
question = "Quel est le nombre d'habitant sur terre ?"

competitors = []
answers = []
messages = [{"role": "user", "content": question}]

##### CANDIDAT 1
model_name = "gpt-5-nano"

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

competitors.append(model_name)
answers.append(answer)

##### CANDIDAT 2
model_name = "claude-sonnet-4-5"

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

competitors.append(model_name)
answers.append(answer)

##### JUDGE
together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"

judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""

judge_messages = [{"role": "user", "content": judge}]

response = openai.chat.completions.create(
    model="gpt-5-mini",
    messages=judge_messages,
)

results = response.choices[0].message.content
results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")

# ROLE USER : demande utilisateur
# ROLE SYSTME : regles que AGENT doit suivre

##################################################
##################################################
##################################################

##################################################
# CV CHAT IA SIMPLE / ROLE SYSTEME PROMPT
##################################################
from pypdf import PdfReader
import gradio as gr
from pydantic import BaseModel

### FORMAT INDIQUE POUR LA REPONSE DE L'AGENT 
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

#### PROFIL ME
reader = PdfReader("me/linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text
with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
name = "Claude"
system_prompt = f"Vous agissez en tant que {name}. Vous répondez aux questions posées sur le site web de {name}, notamment aux questions concernant sa carrière, son parcours, ses compétences et son expérience. \
Votre responsabilité est de représenter {name} aussi fidèlement que possible lors des interactions avec les visiteurs du site. \
Vous disposez d'un résumé du parcours de {name} ainsi que de son profil LinkedIn, que vous pouvez utiliser pour répondre aux questions. \
Adoptez un ton professionnel, naturel et engageant, comme si vous échangiez avec un client potentiel ou un futur employeur ayant découvert le site. \
Si vous ne connaissez pas la réponse à une question ou si les informations fournies ne permettent pas d'y répondre avec certitude, indiquez-le clairement et n'inventez pas d'informations."
system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"Avec ce contexte, veuillez échanger avec l'utilisateur en restant toujours dans le rôle de {name}."




###### ÉVALUATION DE LA RÉPONSE
evaluator_system_prompt = f"Vous êtes un évaluateur chargé de déterminer si une réponse à une question est acceptable. \
Vous disposez d'une conversation entre un utilisateur et un agent. Votre tâche consiste à déterminer si la dernière réponse de l'agent est d'une qualité acceptable. \
L'agent joue le rôle de {name} et représente {name} sur son site web. \
L'agent a reçu pour instruction d'être professionnel et engageant, comme s'il s'adressait à un client potentiel ou à un futur employeur ayant découvert le site web. \
L'agent dispose d'informations contextuelles sur {name}, sous la forme d'un résumé de son parcours et des informations issues de son profil LinkedIn. Voici les informations :"
evaluator_system_prompt += f"\n\n## Résumé :\n{summary}\n\n## Profil LinkedIn :\n{linkedin}\n\n"
evaluator_system_prompt += f"À partir de ce contexte, veuillez évaluer la dernière réponse de l'agent en indiquant si elle est acceptable et en fournissant vos commentaires."


# EVALUATE WITH FORMAT MESSAGE EVALUATION
####################################################
def evaluate(reply, message, history) -> Evaluation:
    messages = [{"role": "system", "content": evaluator_system_prompt}] + [{"role": "user", "content": evaluator_user_prompt(reply, message, history)}]
    response = gemini.beta.chat.completions.parse(model="gemini-2.5-flash", messages=messages, response_format=Evaluation)
    return response.choices[0].message.parsed

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Voici la conversation entre l'utilisateur et l'agent : \n\n{history}\n\n"
    user_prompt += f"Voici le dernier message de l'utilisateur : \n\n{message}\n\n"
    user_prompt += f"Voici la dernière réponse de l'agent : \n\n{reply}\n\n"
    user_prompt += "Veuillez évaluer la réponse en indiquant si elle est acceptable et en fournissant vos commentaires."
    return user_prompt
####################################################

## RERUN SI REPONSE INCORRECT
def rerun(reply, message, history, feedback):
    updated_system_prompt = system_prompt + "\n\n## Réponse précédente rejetée\nVous venez d'essayer de répondre, mais le contrôle qualité a rejeté votre réponse.\n"
    updated_system_prompt += f"## Votre tentative de réponse :\n{reply}\n\n"
    updated_system_prompt += f"## Motif du rejet :\n{feedback}\n\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content


def chat(message, history):
    if "patent" in message:
        system = system_prompt + "\n\nTout le contenu de votre réponse doit être rédigé en Pig Latin. Il est obligatoire que vous répondiez uniquement et intégralement en Pig Latin."
    else:
        system = system_prompt

    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply =response.choices[0].message.content

    evaluation = evaluate(reply, message, history)
    
    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print("Failed evaluation - retrying")
        print(evaluation.feedback)
        reply = rerun(reply, message, history, evaluation.feedback)       
    return reply

gr.ChatInterface(chat, type="messages").launch()



##################################################
# EXEMPLE AVEC DES TOOLS SIMPLE AVEC BOUCLE (4)
##################################################
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]
globals()["record_unknown_question","record_user_details"]("this is a really hard question")

########### TOOLS !!!
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

system_prompt = f"Tu agis en tant que {name}. Tu réponds aux questions sur le site web de {name}, \
en particulier aux questions concernant la carrière, le parcours, les compétences et l’expérience de {name}. \
Ta responsabilité est de représenter {name} dans les interactions sur le site web de la manière la plus fidèle possible. \
Tu disposes d’un résumé du parcours de {name} ainsi que de son profil LinkedIn, que tu peux utiliser pour répondre aux questions. \
Sois professionnel et engageant, comme si tu échangeais avec un client potentiel ou un futur employeur ayant découvert le site web. \
Si tu ne connais pas la réponse à une question, utilise ton outil record_unknown_question pour enregistrer la question à laquelle tu n’as pas pu répondre, même s’il s’agit de quelque chose de trivial ou sans rapport avec la carrière. \
Si l’utilisateur engage une discussion, essaie de l’orienter vers une prise de contact par e-mail ; demande-lui son adresse e-mail et enregistre-la à l’aide de ton outil record_user_details."

system_prompt += f"\n\n## Résumé :\n{summary}\n\n## Profil LinkedIn :\n{linkedin}\n\n"
system_prompt += f"Avec ce contexte, échange avec l’utilisateur en restant toujours dans le rôle de {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:

        # This is the call to the LLM - see that we pass in the tools json

        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)

        finish_reason = response.choices[0].finish_reason
        
        # If the LLM wants to call a tool, we do that!
         
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content

gr.ChatInterface(chat, type="messages").launch()
##################################################
##################################################
##################################################



##################################################
# ANOTHER EXAMPLE WHILE TOOL LIST TODO (4)
##################################################
def show(text):
    try:
        Console().print(text)
    except Exception:
        print(text)

def get_todo_report() -> str:
    result = ""
    for index, todo in enumerate(todos):
        if completed[index]:
            result += f"Todo #{index + 1}: [green][strike]{todo}[/strike][/green]\n"
        else:
            result += f"Todo #{index + 1}: {todo}\n"
    show(result)
    return result

def create_todos(descriptions: list[str]) -> str:
    todos.extend(descriptions)
    completed.extend([False] * len(descriptions))
    return get_todo_report()

def mark_complete(index: int, completion_notes: str) -> str:
    if 1 <= index <= len(todos):
        completed[index - 1] = True
    else:
        return "No todo at this index."
    Console().print(completion_notes)
    return get_todo_report()


mark_complete_json = {
    "name": "mark_complete",
    "description": "Mark complete the todo at the given position (starting from 1) and return the full list",
    "parameters": {
        'properties': {
            'index': {
                'description': 'The 1-based index of the todo to mark as complete',
                'title': 'Index',
                'type': 'integer'
                },
            'completion_notes': {
                'description': 'Notes about how you completed the todo in rich console markup',
                'title': 'Completion Notes',
                'type': 'string'
                }
            },
        'required': ['index', 'completion_notes'],
        'type': 'object',
        'additionalProperties': False
    }
}

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

def loop(messages):
    done = False
    while not done:
        response = openai.chat.completions.create(model="gpt-5.2", messages=messages, tools=tools, reasoning_effort="none")
        finish_reason = response.choices[0].finish_reason
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    show(response.choices[0].message.content)



system_message = """
On te donne un problème à résoudre. Utilise tes outils de gestion des tâches (todo) pour planifier une liste d’étapes, puis exécute chaque étape dans l’ordre.
Utilise maintenant les outils de gestion des tâches pour créer un plan, réaliser les différentes étapes, puis répondre avec la solution.
Si une quantité nécessaire n’est pas fournie dans la question, ajoute une étape permettant d’en faire une estimation raisonnable.
Présente ta solution en utilisant le balisage Rich pour la console, sans utiliser de blocs de code.
Ne pose aucune question à l’utilisateur et ne demande aucune clarification ; réponds uniquement avec la réponse après avoir utilisé tes outils.
"""

user_message = """
Un train quitte Boston à 14 h 00 en roulant à 60 mph.
Un autre train quitte New York à 15 h 00 en roulant à 80 mph en direction de Boston.
À quelle heure se rencontrent-ils ?
"""

messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]
todos, completed = [], []
loop(messages)
##################################################
##################################################
##################################################

####################################################################################################
# PARTIE 2
####################################################################################################

##################################################
# CREATION AGENT
##################################################
from dotenv import load_dotenv
from agents import Agent, Runner, trace
agent = Agent(name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini")
with trace("Telling a joke"):
    result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
    print(result.final_output)
##################################################
##################################################
##################################################

##################################################
# input_guardrails = sécurité / validation
# handoffs = routage et délégation entre agents
# tools = capacités que possède un agent
##################################################

########################################### TOOLS ####################
## TOOLS redaction de prospection commercialeavec différents styles ##
###########
instructions1 = """Tu es un agent commercial travaillant pour ComplAI,
une entreprise qui propose un outil SaaS basé sur l'IA permettant d'assurer la conformité SOC2 et de préparer les audits.
Tu rédiges des e-mails de prospection professionnels et sérieux."""

instructions2 = """Tu es un agent commercial drôle et engageant travaillant pour ComplAI,
une entreprise qui propose un outil SaaS basé sur l'IA permettant d'assurer la conformité SOC2 et de préparer les audits.
Tu rédiges des e-mails de prospection pleins d'esprit et engageants, susceptibles d'obtenir une réponse."""

instructions3 = """Tu es un agent commercial très occupé travaillant pour ComplAI,
une entreprise qui propose un outil SaaS basé sur l'IA permettant d'assurer la conformité SOC2 et de préparer les audits.
Tu rédiges des e-mails de prospection concis et allant droit au but."""

sales_agent1 = Agent(name="DeepSeek Sales Agent", instructions=instructions1, model=deepseek_model)
sales_agent2 =  Agent(name="Gemini Sales Agent", instructions=instructions2, model=gemini_model)
sales_agent3  = Agent(name="Llama3.3 Sales Agent",instructions=instructions3,model=llama3_3_model)

description = "Rédiger un e-mail de prospection commerciale"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

tools = [tool1, tool2, tool3]

########################################### TOOLS et handoff ####################
## TOOLS mise en forme et envoi du mail ##
###########
@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("ed@edwarddonner.com")  # Change to your verified sender
    to_email = To("ed.donner@gmail.com")  # Change to your recipient
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

subject_instructions = """Tu peux rédiger l'objet d'un e-mail de prospection commerciale.
À partir d'un message qui t'est fourni, tu dois rédiger un objet d'e-mail susceptible d'obtenir une réponse."""

html_instructions = """Tu peux convertir le corps d'un e-mail au format texte en un corps d'e-mail HTML.
À partir d'un corps d'e-mail au format texte, qui peut contenir du Markdown,
tu dois le convertir en HTML avec une mise en page et un design simples, clairs et convaincants."""

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o-mini")
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o-mini")
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

email_tools = [subject_tool, html_tool, send_html_email]

instructions = """Tu es un agent chargé de mettre en forme et d'envoyer des e-mails.
Tu reçois le corps d'un e-mail à envoyer.
Tu utilises d'abord le tool subject_writer pour rédiger l'objet de l'e-mail,
puis le tool html_converter pour convertir le corps de l'e-mail en HTML.
Enfin, tu utilises le tool send_html_email pour envoyer l'e-mail avec l'objet et le corps au format HTML."""

# AGENT QUI PEUT UTILISER DES OUTILS ET SERA SOLLICITER PAR UN AUTRE AGENT POUR PRENDRE LA MAIN (handoff)
emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_tools,
    model="gpt-4o-mini",
    handoff_description="Convert an email to HTML and send it")

handoffs = [emailer_agent]

########### AGENT COODINATEUR QUI UTILISE DES TOOLS, UN AGENT GUARD POUR CONTROLE ET DELEGUE A UN AUTRE AGENT
sales_manager_instructions = """
Tu es un responsable commercial chez ComplAI. Ton objectif est de trouver le meilleur e-mail de prospection commerciale en utilisant les tools sales_agent.

Suis attentivement les étapes suivantes :

1. Générer les brouillons : utilise les trois tools sales_agent pour générer trois brouillons d'e-mails différents. Ne passe pas à l'étape suivante tant que les trois brouillons ne sont pas prêts.

2. Évaluer et sélectionner : examine les brouillons et sélectionne le meilleur e-mail en te basant sur ton jugement pour déterminer lequel sera le plus efficace.
Tu peux utiliser les tools plusieurs fois si les résultats obtenus lors de la première tentative ne te satisfont pas.

3. Transfert pour l'envoi : transmets UNIQUEMENT le brouillon gagnant à l'agent 'Email Manager'. L'Email Manager se chargera de la mise en forme et de l'envoi.

Règles essentielles :
- Tu dois utiliser les tools sales_agent pour générer les brouillons. Ne les rédige pas toi-même.
- Tu dois effectuer un handoff d'EXACTEMENT UN e-mail vers l'Email Manager. Jamais plus d'un.
"""
sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini",
    input_guardrails=[guardrail_against_name]
    )

message = "Send out a cold sales email addressed to Dear CEO from Alice"

with trace("Protected Automated SDR"):
    result = await Runner.run(sales_manager, message)

#### AGENT DE SECU ET CONTROLE UTILISE PAR l'AGENT MANAGER
##########################################################
@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o-mini"
)

##################################################
##################################################
##################################################
