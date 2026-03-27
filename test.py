from dotenv import load_dotenv
import os
from ollama import Client
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

# --- CONFIG ---
QUESTION = "Rédige moi un ticket JIRA pour mettre en place un dashboard KPI sur le projet."
MODELS = ["llama3.2", "mistral", "phi3"]  # simulate multi-LLM
OLLAMA_HOST = "http://localhost:11434"

client = Client(host=OLLAMA_HOST)


# --- LLM CALL ---
def call_llm(model: str, prompt: str) -> str:
    try:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False  # plus simple pour gérer
        )
        return response["message"]["content"]
    except Exception as e:
        return f"ERROR with {model}: {str(e)}"


# --- MULTI LLM (PARALLEL) ---
def get_all_answers(question: str, models: list[str]) -> list[dict]:
    results = []

    def task(model):
        print(f"🔹 Asking {model}")
        answer = call_llm(model, question)
        return {"model": model, "answer": answer}

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(task, models))

    return results


# --- FORMAT FOR JUDGE (ANONYMOUS) ---
def build_anonymous_prompt(question: str, answers: list[dict]) -> str:
    formatted = ""

    for i, item in enumerate(answers, start=1):
        formatted += f"# Response {i}\n{item['answer']}\n\n"

    judge_prompt = f"""
Tu es un juge impartial.

Question :
{question}

Voici plusieurs réponses anonymisées :

{formatted}

Ta mission :
1. Classer les réponses de la meilleure à la moins bonne
2. Expliquer ton choix
3. Retourner un JSON STRICT au format :

{{
  "ranking": [1, 2, 3],
  "best": 1,
  "reasoning": "..."
}}
"""
    return judge_prompt


# --- JUDGE ---
def judge_answers(question: str, answers: list[dict], judge_model="llama3.2") -> str:
    prompt = build_anonymous_prompt(question, answers)
    print("⚖️ Judging responses...")
    return call_llm(judge_model, prompt)


# --- MAIN ---
if __name__ == "__main__":
    answers = get_all_answers(QUESTION, MODELS)

    print("\n--- RAW ANSWERS ---")
    for i, a in enumerate(answers, 1):
        print(f"{i}. ({a['model']}) {a['answer'][:100]}...\n")

    result = judge_answers(QUESTION, answers)

    print("\n--- JUDGE RESULT ---")
    print(result)