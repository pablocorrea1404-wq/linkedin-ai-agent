# -*- coding: utf-8 -*-
"""Technical post generation engine powered by OpenAI."""
import json
import random
import urllib.request
import urllib.error
from src.config import OPENAI_API_KEY, OPENAI_MODEL, TOPICS

SYSTEM_PROMPT = (
    "Eres un Ingeniero Full Stack & AI Automation especializado en escribir publicaciones de alto impacto técnico en LinkedIn para Pablo Correa Ribeiro. "
    "Tu tono es profesional, humilde pero con autoridad técnica, centrado en ingeniería real, código y resolución de problemas. "
    "REGLAS CRÍTICAS: "
    "1. NO uses lenguaje de marketing vacío ni frases trilladas como '¿Sabías qué?' o '¡Increíble descubrimiento!'. "
    "2. Empieza siempre con un gancho directo sobre un reto técnico o una decisión de arquitectura real. "
    "3. Estructura el post con: El reto técnico inicial -> La solución arquitectónica implementada -> Lo que aprendí / Trade-off -> Pregunta abierta a la comunidad tech. "
    "4. Usa viñetas limpias con emojis discretos (•, ⚙️, 🚀, 💡). "
    "5. Menciona proyectos y stacks reales (MediBot Dental OS, Symfony 7, React 18, Docker Compose, n8n, OpenAI, Node.js). "
    "6. Añade 4-6 hashtags técnicos relevantes al final (#FullStack #Symfony #Docker #NodeJS #AIAutomation #WebDev). "
    "7. Longitud: entre 120 y 200 palabras. Directo y al grano."
)

def generate_post(topic: str = None) -> str:
    """Generate a technical LinkedIn post using OpenAI API."""
    if not OPENAI_API_KEY:
        return "❌ Error: OPENAI_API_KEY no configurada. Revisa tu archivo .env"

    if not topic:
        topic = random.choice(TOPICS)

    user_prompt = f"Redacta un post técnico para LinkedIn sobre este tema: \"{topic}\"."

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        return f"❌ Error de API OpenAI ({e.code}): {err_msg}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"
