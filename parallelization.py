"""
https://fr.linkedin.com/posts/yassinechabli_9-workflows-agentic-llm-la-plupart-des-gens-activity-7438856556156207104-grKy
https://huggingface.co/blog/dcarpintero/design-patterns-for-building-agentic-workflows
https://www.digitalocean.com/community/tutorials/how-to-build-parallel-agentic-workflows-with-python

Parallélisation
Objectif : Réduire la latence en exécutant plusieurs agents en parallèle.

Fonctionnement : Les tâches sont divisées en plus petits segments, permettant à plusieurs sous-agents de travailler simultanément. 
Par exemple, lors de l'analyse d'un livre volumineux, 100 sous-agents peuvent traiter des chapitres individuels et renvoyer les passages clés pour obtenir des informations plus rapidement.

Utilité : Augmente la vitesse de traitement tout en tirant parti de la puissance collective des agents.

Cas d'usage : Les cabinets d'avocats traitent souvent des milliers de pages de dossiers. Grâce à la parallélisation, un système d'IA peut répartir ces fichiers entre plusieurs agents pour extraire les points clés, réduisant ainsi considérablement le temps nécessaire à la revue.
Cas d'usage : Parallelization for product categorization and tagging across thousands of items.

Exemple : Une entreprise de legal tech utilise cette approche pour résumer des contrats, mettant en évidence les risques et clauses importantes en quelques heures au lieu de plusieurs jours.
"""

import concurrent.futures
import time
from typing import List, Dict
from dotenv import load_dotenv
import os
from ollama import Client
 
load_dotenv()
 
# ----------------------------
# CONFIG
# ----------------------------
MOCK_LLM = False
MAX_WORKERS = 4
CHUNK_SIZE = 100
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # FIX: host local par défaut
OLLAMA_MODEL = "gpt-oss:120b"
 
 
# ----------------------------
# MOCK LLM
# ----------------------------
class MockLLM:
    def generate(self, prompt: str) -> str:
        time.sleep(1)
        return f"[Résumé] {prompt[:50]}..."
 
 
# ----------------------------
# LLM
# ----------------------------
class LLM:
    def __init__(self):
        api_key = os.environ.get("OLLAMA_API_KEY")
        if not api_key:
            raise EnvironmentError("La variable d'environnement OLLAMA_API_KEY est manquante.")
 
        # FIX: une seule instanciation du client
        self.client = Client(
            host=OLLAMA_HOST,
            headers={"Authorization": f"Bearer {api_key}"},
        )
 
    def generate(self, prompt: str) -> str:
        messages = [{"role": "user", "content": f"Resume the text: {prompt}"}]
 
        resume = ""
        # FIX: suppression des args print invalides dans le +=
        for part in self.client.chat(OLLAMA_MODEL, messages=messages, stream=True):
            resume += part["message"]["content"]
 
        return f"[Résumé] {resume}"
 
 
# ----------------------------
# ORCHESTRATOR
# ----------------------------
class Orchestrator:
    def __init__(self, llm: MockLLM | LLM):
        self.llm = llm
 
    def split_text(self, text: str) -> List[str]:
        """Découpe le texte en chunks de taille CHUNK_SIZE."""
        return [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
 
    def dispatch(self, chunks: List[str]) -> List[Dict]:
        """Envoie les chunks aux workers en parallèle, en préservant l'ordre."""
        # FIX: utilisation de map() via executor pour garantir l'ordre des résultats
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(self.worker_task, chunks))
        return results
 
    def worker_task(self, chunk: str) -> Dict:
        """Tâche exécutée par chaque worker, avec gestion d'erreur."""
        try:
            response = self.llm.generate(chunk)
            return {"chunk": chunk, "summary": response, "error": None}
        except Exception as e:
            # FIX: les exceptions dans les threads sont silencieuses sans ce bloc
            print(f"[Worker] Erreur sur le chunk '{chunk[:30]}...' : {e}")
            return {"chunk": chunk, "summary": "", "error": str(e)}
 
 
# ----------------------------
# SYNTHESIZER
# ----------------------------
class Synthesizer:
    def __init__(self, llm: MockLLM | LLM):
        self.llm = llm
 
    def combine(self, results: List[Dict]) -> str:
        """Combine les résumés valides en une synthèse finale."""
        # FIX: on ignore les chunks en erreur plutôt que d'injecter des chaînes vides
        valid_summaries = [r["summary"] for r in results if not r["error"]]
 
        if not valid_summaries:
            raise RuntimeError("Aucun résumé valide à synthétiser.")
 
        combined_text = "\n".join(valid_summaries)
        return self.llm.generate(f"Synthèse globale:\n{combined_text}")
 
 
# ----------------------------
# PIPELINE
# ----------------------------
def run_pipeline(text: str) -> str:
    llm = MockLLM() if MOCK_LLM else LLM()
 
    orchestrator = Orchestrator(llm)
    synthesizer = Synthesizer(llm)
 
    print("1. Découpage du texte...")
    chunks = orchestrator.split_text(text)
    print(f"   → {len(chunks)} chunks de {CHUNK_SIZE} caractères")
 
    print(f"2. Traitement parallèle ({MAX_WORKERS} workers)...")
    results = orchestrator.dispatch(chunks)
 
    errors = [r for r in results if r["error"]]
    if errors:
        print(f"   ⚠ {len(errors)} chunk(s) en erreur sur {len(results)}")
 
    print("3. Synthèse finale...")
    return synthesizer.combine(results)
 
 
# ----------------------------
# EXEMPLE
# ----------------------------
if __name__ == "__main__":
    large_text = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
        "nisi ut aliquip ex ea commodo consequat. "
        "Duis aute irure dolor in reprehenderit in voluptate velit esse "
        "cillum dolore eu fugiat nulla pariatur. "
    ) * 5
 
    result = run_pipeline(large_text)
    print("\nRésultat final :")
    print(result)