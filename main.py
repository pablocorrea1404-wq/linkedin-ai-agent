# -*- coding: utf-8 -*-
"""Main entrypoint for LinkedIn AI Agent daemon."""
import sys
import threading
from src.config import OPENAI_API_KEY, TELEGRAM_BOT_TOKEN
from src.scheduler import run_scheduler_loop
from src.telegram_bot import start_bot_polling

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def print_banner():
    banner = """
============================================================
       LINKEDIN AI CONTENT AGENT (Autonomous Daemon)
   Architecture: OpenAI GPT-4o-mini + Telegram Bot API
   Developer: Pablo Correa Ribeiro (Full Stack & AI Engineer)
============================================================
"""
    print(banner)

def main():
    print_banner()

    # Pre-flight check
    if not OPENAI_API_KEY:
        print("⚠️  AVISO: OPENAI_API_KEY no detectada. Configúrala en tu archivo .env")
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️  AVISO: TELEGRAM_BOT_TOKEN no detectada. Configúrala en tu archivo .env")

    # Iniciar Scheduler en segundo plano (daemon thread)
    scheduler_thread = threading.Thread(target=run_scheduler_loop, daemon=True)
    scheduler_thread.start()

    # Iniciar bucle de Telegram Bot (hilo principal)
    try:
        start_bot_polling()
    except KeyboardInterrupt:
        print("\n👋 Agente detenido manualmente por el usuario. ¡Hasta pronto!")

if __name__ == "__main__":
    main()
