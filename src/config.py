# -*- coding: utf-8 -*-
"""Configuration and environment management module."""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
STATE_PATH = os.path.join(BASE_DIR, 'state.json')

def load_env():
    """Load key-values from .env file with UTF-8 BOM tolerance."""
    env = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip().lstrip('\ufeff')] = v.strip()
    return env

ENV = load_env()

OPENAI_API_KEY = ENV.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
TELEGRAM_BOT_TOKEN = ENV.get('TELEGRAM_BOT_TOKEN', os.getenv('TELEGRAM_BOT_TOKEN', ''))
OPENAI_MODEL = ENV.get('OPENAI_MODEL', os.getenv('OPENAI_MODEL', 'gpt-4o-mini'))
DAILY_SCHEDULE_HOUR = int(ENV.get('DAILY_SCHEDULE_HOUR', os.getenv('DAILY_SCHEDULE_HOUR', '9')))

TOPICS = [
    'Cómo diseñé la arquitectura de MediBot Dental OS (Symfony 7 + React 18 + Docker) para evitar solapamiento de citas médicas',
    'Por qué un desarrollador junior debe dominar Docker Compose antes de saltar a otro framework frontend',
    'De n8n a microservicio en Node.js: Cuándo pivotar un bot transaccional de WhatsApp con OpenAI para máxima resiliencia',
    'OpenAI Function Calling en producción: Cómo hacer que un LLM consulte disponibilidad en tiempo real sin alucinar',
    'Control de concurrencia y seguridad JWT en API Platform: Buenas prácticas aplicadas a un SaaS médico real',
    'Optimización web en producción: Cómo reducir un 30% el tiempo de carga mediante profiling y buenas prácticas',
    'Model Context Protocol (MCP): Por qué los agentes de IA necesitan herramientas estandarizadas y cómo aplicarlo en 2026'
]

def load_state():
    """Load persistent state (registered chat IDs, scheduler flag)."""
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'chat_ids': [], 'daily_active': True, 'last_post': ''}

def save_state(state):
    """Save persistent state safely."""
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Error saving state]: {e}")
