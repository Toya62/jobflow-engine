"""
src/core/notifier.py — Notification module for Karriere Pipeline.
Supports Telegram Bot API for real-time alerts with German local time (Europe/Berlin).
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import urllib.error
import ssl
from zoneinfo import ZoneInfo
from datetime import datetime
from pathlib import Path

# ── Ensure workspace root is in sys.path when executed directly ──────────────
_root_dir = Path(__file__).resolve().parent.parent.parent
if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))

from src.core.logger import get_logger

logger = get_logger(__name__)

GERMAN_TZ = ZoneInfo("Europe/Berlin")

# ── Auto-load local .env if present ──────────────────────────────────────────
from pathlib import Path
_root_dir = Path(__file__).resolve().parent.parent.parent
_env_path = os.path.join(_root_dir, ".env")
if os.path.exists(_env_path):
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))
    except Exception:
        pass


def send_telegram_alert(message: str, bot_token: str = None, chat_id: str = None, parse_mode: str = "Markdown") -> bool:
    """
    Send a message via Telegram Bot API.

    Args:
        message (str): Text message to send. Supports Markdown or HTML.
        bot_token (str, optional): Telegram Bot token. Defaults to TELEGRAM_BOT_TOKEN env.
        chat_id (str, optional): Target chat ID. Defaults to TELEGRAM_CHAT_ID env.
        parse_mode (str): Markdown or HTML parsing mode.

    Returns:
        bool: True if alert dispatched successfully, False otherwise.
    """
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    target_chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not target_chat:
        logger.warning(
            "[Telegram] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured. Alert suppressed. "
            "To activate Telegram alerts, set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env or environment."
        )
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": str(target_chat).strip(),
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "KarrierePipeline/2.0"},
            method="POST",
        )
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            body = resp.read().decode("utf-8")
            if resp.status == 200:
                logger.info(f"[Telegram] Alert successfully dispatched to chat {target_chat}")
                return True
            else:
                logger.error(f"[Telegram] Telegram Bot API returned HTTP {resp.status}: {body}")
                return False
    except Exception as e:
        logger.error(f"[Telegram] Connection error when sending Telegram alert: {e}")
        return False


# Backward compatibility alias for transition
send_alert = send_telegram_alert
send_whatsapp_alert = send_telegram_alert


def notify_scrape_summary(
    new_jobs_count: int = 0,
    approved_count: int = 0,
    portal: str = "all",
    run_approved_count: int = 0,
    run_new_count: int = 0,
    portal_breakdown: dict = None,
    suppress_empty: bool = True,
) -> bool:
    """Format and send a structured scrape & match notification with German Local Time (CEST/CET)."""
    if suppress_empty and run_approved_count == 0 and run_new_count == 0:
        logger.info("[Telegram] Zero fresh jobs and zero approved in this run; summary alert suppressed.")
        return True

    german_time_str = datetime.now(GERMAN_TZ).strftime("%d.%m.%Y, %H:%M CEST")

    breakdown_lines = []
    if portal_breakdown:
        for p_name, p_stats in portal_breakdown.items():
            if p_stats.get("error"):
                breakdown_lines.append(f"   • {p_name}: ⚠️ Error (failed)")
            else:
                p_app = p_stats.get("approved", 0)
                p_scr = p_stats.get("scraped", 0)
                breakdown_lines.append(f"   • {p_name}: +{p_app} approved ({p_scr} fresh)")

    breakdown_text = ("\n" + "\n".join(breakdown_lines) + "\n") if breakdown_lines else "\n"

    msg = (
        f"🚀 *Karriere Pipeline — Scrape Complete*\n\n"
        f"⏰ *Batch Time:* {german_time_str} ({portal.upper()})\n"
        f"✨ *New Approved (This Run):* +{run_approved_count}\n"
        f"📦 *Total Scraped (This Run):* +{run_new_count}"
        f"{breakdown_text}\n"
        f"⭐ *AI Approved (Today):* {approved_count}\n"
        f"📊 *Total Scraped (Today):* {new_jobs_count}"
    )
    return send_telegram_alert(msg)


if __name__ == "__main__":
    test_time = datetime.now(GERMAN_TZ).strftime("%d.%m.%Y, %H:%M CEST")
    test_msg = f"🔔 *Test Alert from Karriere Pipeline*\n\nGerman Time Synchronization Active: *{test_time}*"
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    print(f"Testing Telegram dispatch with token: {'[Set]' if token else '[Not set]'}, chat: {chat or '[Not set]'}")
    success = send_telegram_alert(test_msg)
    if not success:
        print("Note: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env or environment to enable live alerts.")
