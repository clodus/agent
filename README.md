## ENV PYTHON

- python -m venv .venv
- source .venv/Scripts/activate

## 📊 Vue des modèles Ollama

- RAG = LLM + moteur de recherche + tes données

| Modèle | Société | Paramètres | Taille (GB) | Type | Cas d’usage | Date |
|--------|---------|-----------|------------|------|-------------|------|
| qwen3-coder:480b | Alibaba | 480B | 510 | énorme | Génération de code avancée, refactoring massif | 2025-07 |
| ministral-3:8b | Mistral AI | 8B | 10.4 | moyen | Chat, résumé, API légère | 2025-12 |
| devstral-2:123b | Mistral AI | 123B | 128 | très grand | Analyse complexe, RAG avancé | 2025-12 |
| gemma3:12b | Google | 12B | 24 | moyen | Chat général, assistant local | 2025-03 |
| rnj-1:8b | Inconnu | 8B | 16 | moyen | Chat générique | 2025-12 |
| qwen3-vl:235b-instruct | Alibaba | 235B | 470 | énorme | Vision + texte (analyse d’images) | 2025-09 |
| minimax-m2.7 | MiniMax | - | 0 | API | SaaS / non local | 2026-03 |
| gemma3:4b | Google | 4B | 8.6 | léger | Assistant local, usage laptop | 2025-03 |
| nemotron-3-super | NVIDIA | ~200B | 230 | énorme | IA entreprise, analyse massive | 2026-03 |
| glm-4.6 | Zhipu AI | ~600B | 696 | énorme | NLP avancé / recherche | 2025-09 |
| gpt-oss:120b | OpenAI (OSS) | 120B | 65 | grand | Chat avancé, agents IA | 2025-08 |
| qwen3-vl:235b | Alibaba | 235B | 470 | énorme | Multimodal (vision + texte) | 2025-09 |
| minimax-m2.1 | MiniMax | ~200B | 230 | énorme | SaaS entreprise | 2025-12 |
| gemma3:27b | Google | 27B | 55 | grand | Chat avancé en local | 2025-03 |
| cogito-2.1:671b | DeepMind (?) | 671B | 688 | énorme | Raisonnement complexe | 2025-11 |
| glm-4.7 | Zhipu AI | ~600B | 696 | énorme | Recherche avancée | 2025-12 |
| glm-5 | Zhipu AI | ~700B | 756 | énorme | IA nouvelle génération | 2026-02 |
| kimi-k2:1t | Moonshot AI | 1T | 1118 | extrême | Recherche / IA laboratoire | 2025-09 |
| kimi-k2.5 | Moonshot AI | 1T | 1118 | extrême | Raisonnement avancé | 2026-01 |
| qwen3-next:80b | Alibaba | 80B | 81 | grand | Chat + code avancé | 2025-09 |
| qwen3-coder-next | Alibaba | ~80B | 81 | grand | Développement logiciel | 2025-02 |
| deepseek-v3.1:671b | DeepSeek | 671B | 688 | énorme | Raisonnement, math, recherche | 2025-11 |
| deepseek-v3.2 | DeepSeek | 671B | 688 | énorme | Analyse complexe | 2025-12 |
| nemotron-3-nano:30b | NVIDIA | 30B | 32 | moyen | Chat avancé local | 2025-12 |
| ministral-3:3b | Mistral AI | 3B | 4.7 | léger | Chatbot rapide, laptop | 2025-12 |
| ministral-3:14b | Mistral AI | 14B | 15.7 | moyen | Chat + RAG léger | 2025-12 |
| mistral-large-3:675b | Mistral AI | 675B | 682 | énorme | IA entreprise | 2025-12 |
| minimax-m2.5 | MiniMax | ~200B | 230 | énorme | SaaS IA | 2026-02 |
| devstral-small-2:24b | Mistral AI | 24B | 51 | moyen | Analyse de texte, RAG | 2025-12 |
| kimi-k2-thinking | Moonshot AI | 1T | 1118 | extrême | Raisonnement profond | 2025-11 |
| minimax-m2 | MiniMax | ~200B | 230 | énorme | SaaS | 2025-10 |
| gemini-3-flash-preview | Google | - | 0 | API | Chat cloud rapide | 2025-12 |
| gpt-oss:20b | OpenAI (OSS) | 20B | 13.7 | moyen | Chat + agents simples | 2025-08 |
| qwen3.5:397b | Alibaba | 397B | 397 | énorme | IA avancée | 2026-02 |

### 🧠 Modèles recommandés en local

#### 💻 Léger (Laptop / CPU)
- ministral-3:3b
- gemma3:4b

#### ⚙️ Intermédiaire (GPU standard)
- ministral-3:8b
- ministral-3:14b
- gpt-oss:20b

#### 🚀 Avancé (GPU haut de gamme)
- nemotron-3-nano:30b
- gemma3:27b

> ⚠️ Les modèles > 100GB ne sont pas adaptés à un usage local sans infrastructure distribuée.

## 📊 Autres modèles LLM du marché

| Modèle | Société | Paramètres | Taille (GB) | Type | Cas d’usage | Date |
|--------|---------|-----------|------------|------|-------------|------|
| llama-3:70b | Meta | 70B | ~140 | grand | Chat, fine-tuning, local / self-hosting | 2024-04 |
| llama-4:70b+ | Meta | 70B–405B | ~150–800 | très grand | Applications générales, agents IA | 2026-01 |
| mixtral-8x22b | Mistral AI | MoE (~140B actif) | ~90 | grand | Chat performant, coût optimisé | 2024-12 |
| mistral-small-3:24b | Mistral AI | 24B | ~50 | moyen | Chat rapide, temps réel | 2025-01 |
| deepseek-r1 | DeepSeek | ~100B+ | ~100 | très grand | Raisonnement, math, code | 2025-01 |
| deepseek-coder | DeepSeek | 33B | ~35 | moyen | Génération de code | 2024-06 |
| qwen-2.5:72b | Alibaba | 72B | ~80 | grand | Chat, multilingue | 2025-02 |
| qwen-coder | Alibaba | 7B–32B | ~10–40 | léger à moyen | Développement logiciel | 2024-09 |
| gemma-2:9b | Google | 9B | ~18 | moyen | Chat local, assistant | 2024-05 |
| gemini-1.5-pro | Google | - | 0 | API | Multimodal, analyse longue | 2024-06 |
| gemini-3-pro | Google | - | 0 | API | Multimodal avancé, agents | 2025-12 |
| claude-3-opus | Anthropic | - | 0 | API | Analyse complexe, rédaction | 2024-03 |
| claude-3.5-sonnet | Anthropic | - | 0 | API | Code, chat, productivité | 2024-10 |
| claude-4 | Anthropic | - | 0 | API | Raisonnement avancé | 2025-12 |
| gpt-4o | OpenAI | - | 0 | API | Chat multimodal rapide | 2024-05 |
| gpt-5 | OpenAI | - | 0 | API | Raisonnement, agents IA | 2025-12 |
| command-r+ | Cohere | ~100B | ~100 | grand | RAG, entreprise | 2024-04 |
| command-a | Cohere | ~50B | ~60 | moyen | Recherche, NLP entreprise | 2025-01 |
| grok-2 | xAI | - | 0 | API | Chat temps réel (X/Twitter) | 2024-11 |
| grok-3 | xAI | - | 0 | API | Analyse live, actualités | 2025-12 |
| ernie-4.0 | Baidu | ~100B | ~100 | grand | NLP chinois, entreprise | 2024-06 |
| hunyuan | Tencent | ~100B | ~100 | grand | Chat, services cloud | 2024-09 |
| yi-34b | 01.AI | 34B | ~40 | moyen | Chat open source performant | 2024-03 |
| olmo-7b | AI2 (Allen Institute) | 7B | ~14 | léger | Recherche open source pur | 2024-02 |
| mpt-30b | MosaicML | 30B | ~60 | moyen | NLP, fine-tuning | 2023-12 |
| falcon-40b | TII (UAE) | 40B | ~80 | grand | Chat, open source | 2023-09 |
| bloom | BigScience | 176B | ~350 | énorme | Recherche, multilingue | 2023-07 |

## 📊 Modèles LLM installables en local

| Modèle | Société | Paramètres | Taille (GB) | Type | Cas d’usage | Date |
|--------|---------|-----------|------------|------|-------------|------|
| llama-3:70b | Meta | 70B | ~140 | grand | Chat, fine-tuning, self-hosting | 2024-04 |
| llama-4:70b+ | Meta | 70B–405B | ~150–800 | très grand | Applications générales, agents IA | 2026-01 |
| mixtral-8x22b | Mistral AI | MoE (~140B actif) | ~90 | grand | Chat performant, coût optimisé | 2024-12 |
| mistral-small-3:24b | Mistral AI | 24B | ~50 | moyen | Chat rapide, temps réel | 2025-01 |
| devstral-2:123b | Mistral AI | 123B | 128 | très grand | Analyse complexe, RAG avancé | 2025-12 |
| devstral-small-2:24b | Mistral AI | 24B | 51 | moyen | Analyse de texte, RAG | 2025-12 |
| ministral-3:3b | Mistral AI | 3B | 4.7 | léger | Chatbot rapide, laptop | 2025-12 |
| ministral-3:8b | Mistral AI | 8B | 10.4 | moyen | Chat, résumé, API légère | 2025-12 |
| ministral-3:14b | Mistral AI | 14B | 15.7 | moyen | Chat + RAG léger | 2025-12 |
| qwen3-coder:480b | Alibaba | 480B | 510 | énorme | Génération de code avancée, refactoring massif | 2025-07 |
| qwen3-vl:235b | Alibaba | 235B | 470 | énorme | Multimodal (vision + texte) | 2025-09 |
| qwen3-vl:235b-instruct | Alibaba | 235B | 470 | énorme | Vision + texte (analyse d’images) | 2025-09 |
| qwen3-next:80b | Alibaba | 80B | 81 | grand | Chat + code avancé | 2025-09 |
| qwen3-coder-next | Alibaba | ~80B | 81 | grand | Développement logiciel | 2025-02 |
| gemma3:4b | Google | 4B | 8.6 | léger | Assistant local, usage laptop | 2025-03 |
| gemma3:12b | Google | 12B | 24 | moyen | Chat général, assistant local | 2025-03 |
| gemma3:27b | Google | 27B | 55 | grand | Chat avancé en local | 2025-03 |
| nemotron-3-nano:30b | NVIDIA | 30B | 32 | moyen | Chat avancé local | 2025-12 |
| nemotron-3-super | NVIDIA | ~200B | 230 | énorme | IA entreprise, analyse massive | 2026-03 |
| kimi-k2:1t | Moonshot AI | 1T | 1118 | extrême | Recherche / IA laboratoire | 2025-09 |
| kimi-k2.5 | Moonshot AI | 1T | 1118 | extrême | Raisonnement avancé | 2026-01 |
| kimi-k2-thinking | Moonshot AI | 1T | 1118 | extrême | Raisonnement profond | 2025-11 |
| mpt-30b | MosaicML | 30B | 60 | moyen | NLP, fine-tuning | 2023-12 |
| falcon-40b | TII (UAE) | 40B | 80 | grand | Chat, open source | 2023-09 |
| bloom | BigScience | 176B | 350 | énorme | Recherche, multilingue | 2023-07 |
| olmo-7b | AI2 (Allen Institute) | 7B | 14 | léger | Recherche open source pur | 2024-02 |
| yi-34b | 01.AI | 34B | 40 | moyen | Chat open source performant | 2024-03 |

## 🤖 Guide de choix LLM selon le cas d’usage

| Cas d’usage | Modèles recommandés | Taille / Ressources | Notes |
|-------------|------------------|------------------|------|
| Chat simple local / test | gemma3:4b, ministral-3:3b, olmo-7b | Léger (CPU/laptop ou petit GPU) | Rapide, bon pour prototypes et chat local |
| Chat avancé / assistant | gemma3:12b, ministral-3:8b, mpt-30b | Moyen (GPU 24–32GB) | Réponses plus cohérentes, multi-turn dialogue |
| Chat multilingue / recherche documentaire | bloom, gemma3:27b, devstral-2:123b | Grand (GPU 40–80GB) | Bonne couverture linguistique et compréhension contextuelle |
| RAG / Base de connaissances interne | devstral-2:123b, ministral-3:14b, mixtral-8x22b | Moyen → grand | Combine récupération + génération pour info précise |
| Génération de code | qwen3-coder:480b, qwen3-coder-next | Grand → énorme | Refactoring, génération complexe, support multi-langages |
| Analyse massive / recherche scientifique | nemotron-3-super, kimi-k2:1t, kimi-k2.5 | Extrême (GPU ≥ 80GB / multi-GPU) | Idéal pour datasets volumineux ou IA recherche |
| Vision + Texte (Multimodal) | qwen3-vl:235b, qwen3-vl:235b-instruct | Grand → énorme | Analyse images + texte, reconnaissance de contenu |
| Prototype rapide / laptop | ministral-3:3b, gemma3:4b, olmo-7b | Léger | Idéal pour test rapide et faible consommation |
| SaaS / Cloud deployment | MiniMax (M2, M2.1, M2.5) | API / cloud | Pas local, mais scalable et prêt à l’emploi |