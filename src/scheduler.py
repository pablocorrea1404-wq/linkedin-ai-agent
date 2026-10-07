# -*- coding: utf-8 -*-
"""Daily automated dispatch scheduler."""
import time
from datetime import datetime
from src.config import DAILY_SCHEDULE_HOUR, load_state, save_state
from src.generator import generate_post
from src.telegram_bot import send_post_preview

def check_and_dispatch():
    """Evaluate if daily morning post should be dispatched to registered users."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    state = load_state()
    if not state.get("daily_active", True):
        return

    chat_ids = state.get("chat_ids", [])
    if not chat_ids:
        return

    # Check if hour matches and post hasn't been sent today
    if now.hour == DAILY_SCHEDULE_HOUR and state.get("last_dispatch_date") != today_str:
        print(f"⏰ [Scheduler] Disparando publicación matutina programada para {len(chat_ids)} chats...")
        post = generate_post()
        state["last_post"] = post
        state["last_dispatch_date"] = today_str
        save_state(state)

        for chat_id in chat_ids:
            try:
                send_post_preview(chat_id, post)
                print(f"✅ [Scheduler] Post enviado al chat {chat_id}")
            except Exception as e:
                print(f"❌ [Scheduler] Error enviando a {chat_id}: {e}")

def run_scheduler_loop():
    """Continuous scheduler loop checking periodically."""
    print(f"⏰ [Scheduler] Motor activo (Programado para las {DAILY_SCHEDULE_HOUR:02d}:00 cada mañana)...")
    while True:
        try:
            check_and_dispatch()
        except Exception as e:
            print(f"[Scheduler Exception]: {e}")
        time.sleep(60)
