"""Clients LLM unifies pour le TP4 : un meme appel chat() vers 4 fournisseurs.

Fournisseurs (choisis via l'argument `provider`) :
  - "openai"  : API OpenAI (ChatGPT)   -> SDK `openai`
  - "gemini"  : API Google Gemini      -> SDK `google-generativeai`
  - "claude"  : API Anthropic (Claude) -> SDK `anthropic`
  - "local"   : modele local via Ollama (ou tout serveur compatible OpenAI)

Les cles API sont lues dans les variables d'environnement (voir .env.example).
Aucune cle n'est ecrite dans le code : on ne versionne JAMAIS un secret.

Tous les fournisseurs exposent la MEME signature :
    chat(provider, prompt, system=None, temperature=0.7, max_tokens=512) -> str
ce qui permet de comparer les techniques de prompting a fournisseur constant,
ou un meme prompt sur les 4 fournisseurs.
"""
from __future__ import annotations

import os

# Charge automatiquement un fichier .env s'il existe (cles API, endpoint local).
# Si python-dotenv n'est pas installe, le .env n'est PAS lu : on previent au lieu
# d'echouer en silence (sinon aucun fournisseur n'est detecte et on obtient None).
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    import warnings

    warnings.warn(
        "python-dotenv absent : le fichier .env n'a PAS ete charge, "
        "les variables (cles API, LOCAL_BASE_URL) ne seront pas lues. "
        "Installez les dependances du TP4 : `make install-llm`.",
        stacklevel=2,
    )

PROVIDERS = ("openai", "gemini", "claude", "local")


def disponible(provider: str) -> bool:
    """Vrai si la cle API (ou l'endpoint local) necessaire est configuree."""
    provider = provider.lower()
    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    if provider == "gemini":
        return bool(os.getenv("GEMINI_API_KEY"))
    if provider == "claude":
        return bool(os.getenv("ANTHROPIC_API_KEY"))
    if provider == "local":
        return bool(os.getenv("LOCAL_BASE_URL"))
    raise ValueError(f"Fournisseur inconnu : {provider!r} (attendu : {PROVIDERS})")


def modele(provider: str) -> str:
    """Nom du modele utilise pour ce fournisseur (surchargeable par variable d'env)."""
    return {
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "gemini": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        "claude": os.getenv("CLAUDE_MODEL", "claude-opus-4-8"),
        "local": os.getenv("LOCAL_MODEL", "llama3.1"),
    }[provider.lower()]


def chat(
    provider: str,
    prompt: str,
    system: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> str:
    """Envoie `prompt` (+ eventuel `system`) au fournisseur et renvoie le texte."""
    provider = provider.lower()
    if provider == "openai":
        return _openai_compatible(prompt, system, temperature, max_tokens, local=False)
    if provider == "local":
        return _openai_compatible(prompt, system, temperature, max_tokens, local=True)
    if provider == "gemini":
        return _gemini(prompt, system, temperature, max_tokens)
    if provider == "claude":
        return _claude(prompt, system, temperature, max_tokens)
    raise ValueError(f"Fournisseur inconnu : {provider!r} (attendu : {PROVIDERS})")


# --------------------------------------------------------------------------
# Implementations par fournisseur (imports parasols : erreur claire si absent)
# --------------------------------------------------------------------------
def _openai_compatible(prompt, system, temperature, max_tokens, local):
    """OpenAI (ChatGPT) et modeles locaux : meme API `chat.completions`.

    Ollama expose un endpoint compatible OpenAI sur http://localhost:11434/v1,
    donc le meme SDK sert pour "openai" et pour "local" (seule l'URL change).
    """
    from openai import OpenAI

    if local:
        client = OpenAI(
            base_url=os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("LOCAL_API_KEY", "ollama"),  # Ollama ignore la cle
        )
        model = os.getenv("LOCAL_MODEL", "llama3.1")
    else:
        client = OpenAI()  # lit OPENAI_API_KEY dans l'environnement
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    return (resp.choices[0].message.content or "").strip()


def _gemini(prompt, system, temperature, max_tokens):
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        system_instruction=system,  # None accepte
    )
    resp = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
    )
    return (resp.text or "").strip()


def _claude(prompt, system, temperature, max_tokens):
    import anthropic

    client = anthropic.Anthropic()  # lit ANTHROPIC_API_KEY dans l'environnement
    kwargs = {
        "model": os.getenv("CLAUDE_MODEL", "claude-opus-4-8"),
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    # NB : sur Claude Opus 4.8 / Sonnet 5, le parametre `temperature` n'est PAS
    # accepte (erreur 400) -> on ne le transmet pas ; la variance se pilote par
    # le prompt. Sur des modeles plus anciens on pourrait le passer.
    resp = client.messages.create(**kwargs)
    return "".join(b.text for b in resp.content if b.type == "text").strip()
