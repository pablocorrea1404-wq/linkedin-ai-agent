# -*- coding: utf-8 -*-
"""Telegram Bot interface and polling engine."""
import time
import json
import urllib.request
import urllib.error
from src.config import TELEGRAM_BOT_TOKEN, TOPICS, load_state, save_state
from src.generator import generate_post

def telegram_api(method: str, params: dict = None) -> dict:
    """Send an API request to Telegram Bot API."""
    if not TELEGRAM_BOT_TOKEN:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN no configurado"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    if params:
        data = json.dumps(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_post_preview(chat_id: int, post_text: str):
    """Send a generated post with interactive action buttons."""
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🚀 Abrir LinkedIn para Publicar", "url": "https://www.linkedin.com/feed/"}
            ],
            [
                {"text": "🔄 Generar Otro Post", "callback_data": "action_regenerate"},
                {"text": "💡 Elegir Tema", "callback_data": "action_topics"}
            ]
        ]
    }
    msg = f"📝 **PROPUESTA TÉCNICA LISTA PARA PUBLICAR:**\n\n{post_text}\n\n---\n👆 *Copia el texto arriba y pulsa el botón para abrir LinkedIn.*"
    return telegram_api("sendMessage", {
        "chat_id": chat_id,
        "text": msg,
        "reply_markup": reply_markup,
        "disable_web_page_preview": True
    })

def handle_update(upd: dict):
    """Process incoming Telegram updates (messages & callback queries)."""
    state = load_state()

    # 1. Mensajes de texto
    if "message" in upd:
        msg = upd["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "").strip()

        if chat_id not in state["chat_ids"]:
            state["chat_ids"].append(chat_id)
            save_state(state)

        if text.startswith("/start"):
            welcome = (
                "👋 **¡Hola! Soy tu Agente Autónomo de Contenido para LinkedIn.**\n\n"
                "Estoy programado para ayudarte a construir autoridad técnica publicando aprendizajes reales sobre arquitectura de software, Docker, Symfony, React, n8n e IA.\n\n"
                "📌 **Comandos disponibles:**\n"
                "• `/generar` ➔ Genera un post técnico de inmediato.\n"
                "• `/temas` ➔ Explora y selecciona temas técnicos concretos.\n"
                "• Cada mañana a las 09:00h te enviaré un borrador automático para publicar en un clic."
            )
            telegram_api("sendMessage", {
                "chat_id": chat_id,
                "text": welcome,
                "reply_markup": {
                    "keyboard": [
                        [{"text": "🚀 Generar Post Ahora"}, {"text": "💡 Ver Temas"}],
                        [{"text": "ℹ️ Ayuda"}]
                    ],
                    "resize_keyboard": True
                }
            })

        elif text in ["/generar", "🚀 Generar Post Ahora"]:
            telegram_api("sendMessage", {"chat_id": chat_id, "text": "⏳ Conectando con OpenAI y analizando arquitectura..."})
            post = generate_post()
            state["last_post"] = post
            save_state(state)
            send_post_preview(chat_id, post)

        elif text in ["/temas", "💡 Ver Temas"]:
            t_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(TOPICS)])
            telegram_api("sendMessage", {
                "chat_id": chat_id,
                "text": f"💡 **Temas técnicos disponibles:**\n\n{t_list}\n\n👉 Escribe el número del tema (ej. 1, 2, 3...) para generarlo directamente."
            })

        elif text.isdigit() and 1 <= int(text) <= len(TOPICS):
            idx = int(text) - 1
            chosen_topic = TOPICS[idx]
            telegram_api("sendMessage", {"chat_id": chat_id, "text": f"⏳ Redactando post sobre: \"{chosen_topic}\"..."})
            post = generate_post(chosen_topic)
            state["last_post"] = post
            save_state(state)
            send_post_preview(chat_id, post)

        else:
            telegram_api("sendMessage", {
                "chat_id": chat_id,
                "text": "Pulsa /generar para crear un post de LinkedIn o escribe el número de un tema."
            })

    # 2. Botones interactivos (Callback queries)
    elif "callback_query" in upd:
        cb = upd["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb.get("data", "")

        telegram_api("answerCallbackQuery", {"callback_query_id": cb["id"]})

        if data == "action_regenerate":
            telegram_api("sendMessage", {"chat_id": chat_id, "text": "🔄 Generando nueva propuesta técnica..."})
            post = generate_post()
            state["last_post"] = post
            save_state(state)
            send_post_preview(chat_id, post)

        elif data == "action_topics":
            t_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(TOPICS)])
            telegram_api("sendMessage", {
                "chat_id": chat_id,
                "text": f"💡 **Elige un tema escribiendo su número:**\n\n{t_list}"
            })

def start_bot_polling():
    """Start continuous polling loop for Telegram."""
    offset = 0
    print("🤖 [Telegram Bot] Polling iniciado con éxito...")
    while True:
        try:
            res = telegram_api("getUpdates", {"offset": offset, "timeout": 20})
            if res.get("ok") and res.get("result"):
                for item in res["result"]:
                    offset = item["update_id"] + 1
                    handle_update(item)
            time.sleep(1)
        except Exception as e:
            print(f"[Telegram Polling Error]: {e}")
            time.sleep(3)
