"""
DURGAM Telegram Notification Service
=====================================
Sovereign cyber-defence real-time alert dispatcher via Telegram Bot API.

Alert categories:
  • 🚨 New complaint filed (citizen desk)
  • ⛓️ Micro-hold placed (bank switch)
  • 🚀 CAD patrol dispatch (police tactical)
  • ⚠️  ATM cashout threat (predictive radar)
  • ✅ Restitution / fund recovery confirmed

Usage:
    from backend.app.services.telegram_service import telegram_bot
    await telegram_bot.send_complaint_alert(complaint_data)

Configuration (.env):
    TELEGRAM_BOT_TOKEN       — Bot HTTP API token from @BotFather
    TELEGRAM_POLICE_CHAT_ID  — Chat/group ID to receive police alerts
    TELEGRAM_CMD_CHAT_ID     — (Optional) I4C command war room group ID
    TELEGRAM_BANK_CHAT_ID    — (Optional) Bank nodal officer group ID
"""

import os
import asyncio
import httpx
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger("durgam.telegram")


class DurgamTelegramBot:
    """Async Telegram Bot notification client for DURGAM platform."""

    def __init__(self):
        self.reload_config()

    def reload_config(self):
        from dotenv import load_dotenv
        load_dotenv(override=True)
        self.token: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self._police_chat_id: str = os.getenv("TELEGRAM_POLICE_CHAT_ID", "").strip()
        self._cmd_chat_id: str = os.getenv("TELEGRAM_CMD_CHAT_ID", "").strip()
        self._bank_chat_id: str = os.getenv("TELEGRAM_BANK_CHAT_ID", "").strip()
        self.officer_name: str = os.getenv("POLICE_OFFICER_NAME", "SI Rajesh Hooda / PCR Falcon 1")
        self._base_url: str = f"https://api.telegram.org/bot{self.token}"
        self._enabled: bool = bool(self.token and self.token not in ("", "PASTE_NEW_TOKEN_HERE", "your_telegram_bot_token_here"))

    @property
    def police_chat_id(self) -> str:
        return os.getenv("TELEGRAM_POLICE_CHAT_ID", self._police_chat_id or "").strip()

    @property
    def cmd_chat_id(self) -> str:
        return os.getenv("TELEGRAM_CMD_CHAT_ID", self._cmd_chat_id or self.police_chat_id).strip()

    @property
    def bank_chat_id(self) -> str:
        return os.getenv("TELEGRAM_BANK_CHAT_ID", self._bank_chat_id or self.police_chat_id).strip()


    # ──────────────────────────────────────────────
    #  Core send method
    # ──────────────────────────────────────────────

    async def _send(self, chat_id: str, text: str, parse_mode: str = "HTML") -> bool:
        """Low-level: POST sendMessage to Telegram Bot API."""
        if not self._enabled:
            logger.warning("Telegram bot token not configured — alert suppressed.")
            return False
        if not chat_id or chat_id in ("", "your_telegram_chat_id_here"):
            logger.warning("Telegram chat_id not configured — alert suppressed.")
            return False

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(f"{self._base_url}/sendMessage", json=payload)
                data = resp.json()
                if not data.get("ok"):
                    logger.error(f"Telegram API error: {data.get('description')}")
                    return False
                logger.info(f"Telegram alert sent to {chat_id}")
                return True
        except httpx.RequestError as exc:
            logger.error(f"Telegram network error: {exc}")
            return False

    def _send_sync_worker(self, chat_id: str, text: str, parse_mode: str = "HTML"):
        """Background worker executing synchronous HTTP post."""
        if not self._enabled or not chat_id or chat_id in ("", "your_telegram_chat_id_here"):
            return
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(f"{self._base_url}/sendMessage", json=payload)
                data = resp.json()
                if not data.get("ok"):
                    logger.warning(f"Telegram API response: {data.get('description')}")
                else:
                    logger.info(f"Telegram alert delivered to {chat_id}")
        except Exception as exc:
            logger.warning(f"Telegram network note: {exc}")

    def send_sync(self, chat_id: str, text: str) -> bool:
        """Non-blocking fire-and-forget background dispatcher for synchronous routes."""
        import threading
        if not self._enabled or not chat_id or chat_id in ("", "your_telegram_chat_id_here"):
            return False
        try:
            threading.Thread(target=self._send_sync_worker, args=(chat_id, text), daemon=True).start()
            return True
        except Exception as exc:
            logger.error(f"Telegram send_sync thread error: {exc}")
            return False

    # ──────────────────────────────────────────────
    #  Alert Templates
    # ──────────────────────────────────────────────

    def send_complaint_alert(self, complaint: Dict[str, Any]) -> bool:
        """🚨 Citizen files a cybercrime complaint → notify I4C Command."""
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")
        amount_inr = complaint.get("loss_amount", 0)
        amount_fmt = f"₹{amount_inr:,.0f}" if isinstance(amount_inr, (int, float)) else str(amount_inr)

        text = (
            "🚨 <b>NEW CYBERCRIME COMPLAINT — DURGAM I4C</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>FIR No:</b> <code>{complaint.get('ack_number', 'N/A')}</code>\n"
            f"👤 <b>Victim:</b> {complaint.get('victim_name', 'N/A')}\n"
            f"📱 <b>Mobile:</b> <code>{complaint.get('victim_mobile', 'N/A')}</code>\n"
            f"💰 <b>Loss Amount:</b> <b>{amount_fmt}</b>\n"
            f"🏦 <b>Suspect Account:</b> <code>{complaint.get('to_account', 'N/A')}</code>\n"
            f"🔍 <b>Crime Type:</b> {complaint.get('fraud_type', 'N/A')}\n"
            f"🗺️ <b>State:</b> {complaint.get('victim_state', 'N/A')}\n"
            f"🕐 <b>Filed:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ <i>Golden-Hour interception pipeline activated.</i>"
        )
        return self.send_sync(self.cmd_chat_id, text)

    def send_micro_hold_alert(self, hold: Dict[str, Any]) -> bool:
        """⛓️ Bank micro-hold placed → notify police and bank nodal."""
        amount_fmt = f"₹{hold.get('hold_amount', 0):,.0f}"
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")

        text = (
            "⛓️ <b>MICRO-HOLD PLACED — DURGAM SWITCH</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Case:</b> <code>{hold.get('case_id', 'N/A')}</code>\n"
            f"🏦 <b>Bank:</b> {hold.get('bank_name', 'N/A')}\n"
            f"💳 <b>Account Frozen:</b> <code>{hold.get('account_number', 'N/A')}</code>\n"
            f"💰 <b>Amount Quarantined:</b> <b>{amount_fmt}</b>\n"
            f"⚡ <b>Latency:</b> {hold.get('latency_ms', 'N/A')} ms\n"
            f"📜 <b>ISO Ref:</b> <code>{hold.get('iso_ref', 'camt.056')}</code>\n"
            f"🕐 <b>Time:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <i>Pre-settlement lien active. Funds secured pending court order.</i>"
        )
        return self.send_sync(self.police_chat_id, text)

    def send_cad_dispatch_alert(self, dispatch: Dict[str, Any]) -> bool:
        """🚀 Patrol unit dispatched to ATM → notify field officers."""
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")

        text = (
            "🚀 <b>FALCON CAD DISPATCH — POLICE TACTICAL</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>Target ATM:</b> <code>{dispatch.get('atm_id', 'N/A')}</code>\n"
            f"📍 <b>Location:</b> {dispatch.get('atm_location', 'N/A')}\n"
            f"🚨 <b>Risk Score:</b> <b>{dispatch.get('risk_score', 'N/A')}</b>\n"
            f"🚗 <b>Unit Assigned:</b> {dispatch.get('unit', self.officer_name)}\n"
            f"⏱️ <b>ETA:</b> {dispatch.get('eta_minutes', '?')} minutes\n"
            f"📡 <b>GPS:</b> {dispatch.get('lat', '?')}, {dispatch.get('lon', '?')}\n"
            f"🕐 <b>Dispatch Time:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ <i>Intercept in progress. Report status on arrival.</i>"
        )
        return self.send_sync(self.police_chat_id, text)

    def send_atm_threat_alert(self, atm: Dict[str, Any]) -> bool:
        """⚠️ ST-KDE high-risk ATM threshold breached → broadcast."""
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")

        text = (
            "⚠️ <b>ATM CASHOUT THREAT — ST-KDE RADAR</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏧 <b>ATM:</b> <code>{atm.get('atm_id', 'N/A')}</code>\n"
            f"📍 <b>Location:</b> {atm.get('name', 'N/A')}\n"
            f"🔴 <b>Risk Score:</b> <b>{atm.get('risk_score', 'N/A')}</b>\n"
            f"⏱️ <b>Predicted Window:</b> {atm.get('eta_minutes', '?')} mins\n"
            f"🗺️ <b>Jurisdiction:</b> {atm.get('jurisdiction', 'N/A')}\n"
            f"🤖 <b>Model:</b> XGBoost + Gaussian KDE v2.1\n"
            f"🕐 <b>Generated:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🚨 <i>Dispatch patrol unit immediately to prevent cashout.</i>"
        )
        return self.send_sync(self.cmd_chat_id, text)

    def send_restitution_alert(self, case: Dict[str, Any]) -> bool:
        """✅ Fund restitution confirmed → notify victim and officers."""
        amount_fmt = f"₹{case.get('recovered_amount', 0):,.0f}"
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")

        text = (
            "✅ <b>FUND RESTITUTION CONFIRMED — DURGAM</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Case:</b> <code>{case.get('case_id', 'N/A')}</code>\n"
            f"👤 <b>Victim:</b> {case.get('victim_name', 'N/A')}\n"
            f"💰 <b>Recovered:</b> <b>{amount_fmt}</b>\n"
            f"⛓️ <b>Hold Released By:</b> Cyber Court Decree\n"
            f"🔗 <b>Merkle Hash:</b> <code>{case.get('merkle_hash', 'N/A')[:24]}…</code>\n"
            f"🕐 <b>Confirmed:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🏛️ <i>Immutable evidence sealed on Polygon Amoy blockchain.</i>"
        )
        return self.send_sync(self.cmd_chat_id, text)

    def send_police_turn_by_turn_dispatch(
        self,
        complaint_id: str,
        unit_id: str = "PCR_FALCON_1",
        atm_data: Optional[Dict[str, Any]] = None,
        amount: float = 250000.0,
        mule_account: str = "MULE_90214810",
        eta_minutes: int = 4,
        confidence_score: float = 0.942,
        chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """🚨 Field Police CAD Tactical Turn-by-Turn GPS Dispatch Alert."""
        atm = atm_data or {}
        atm_name = atm.get("name") or atm.get("bank_name", "SBI ATM Sector 29 Market")
        atm_addr = atm.get("address") or atm.get("location_name", "Sector 29 Market, Gurugram, Delhi NCR")
        lat = atm.get("lat") or atm.get("latitude") or 28.4595
        lon = atm.get("lon") or atm.get("longitude") or 77.0266
        nav_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
        amount_fmt = f"₹{amount:,.0f}" if isinstance(amount, (int, float)) else str(amount)
        conf_pct = f"{confidence_score * 100:.1f}%" if confidence_score <= 1.0 else f"{confidence_score}%"
        ts = datetime.now().strftime("%d %b %Y %H:%M IST")

        text = (
            "🚨 <b>TACTICAL TURN-BY-TURN DISPATCH — DURGAM CAD</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Complaint / FIR:</b> <code>{complaint_id}</code>\n"
            f"🚓 <b>Assigned Unit:</b> <b>{unit_id}</b> ({self.officer_name})\n"
            f"🏧 <b>Target ATM:</b> <b>{atm_name}</b>\n"
            f"📍 <b>Address:</b> {atm_addr}\n"
            f"⏱️ <b>ETA:</b> <b>{eta_minutes} Minutes</b>\n"
            f"🎯 <b>ST-KDE Risk Score:</b> <b>{conf_pct}</b>\n"
            f"💳 <b>Mule Account:</b> <code>{mule_account}</code>\n"
            f"💰 <b>Loss Amount:</b> <b>{amount_fmt}</b>\n"
            f"🗺️ <b>GPS Navigation:</b> <a href=\"{nav_url}\">Open Turn-by-Turn GPS Map</a>\n"
            f"🕐 <b>Dispatch Time:</b> {ts}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚖️ <i>Mandate: Sec 106 BNSS 2023 / Sec 318(4) BNS. Intercept suspect at ATM kiosk.</i>"
        )

        target_chat = chat_id if (chat_id and not str(chat_id).startswith("@")) else self.police_chat_id
        sent = self.send_sync(target_chat, text)
        return {
            "status": "DISPATCHED" if sent else "TRANSMITTED_LOCAL",
            "telegram_sent": sent,
            "complaint_id": complaint_id,
            "unit_id": unit_id,
            "target_atm": atm_name,
            "navigation_url": nav_url,
            "eta_minutes": eta_minutes,
            "lat": lat,
            "lon": lon
        }

    # ──────────────────────────────────────────────
    #  Bot Management
    # ──────────────────────────────────────────────

    async def get_me(self) -> Optional[Dict]:
        """Verify bot token and return bot info."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self._base_url}/getMe")
                data = resp.json()
                if data.get("ok"):
                    return data["result"]
                return None
        except Exception:
            return None

    async def get_updates(self, offset: int = 0) -> list:
        """Poll for incoming messages (for chat_id discovery)."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"{self._base_url}/getUpdates",
                    params={"offset": offset, "limit": 10, "timeout": 0}
                )
                data = resp.json()
                return data.get("result", []) if data.get("ok") else []
        except Exception:
            return []

    def is_configured(self) -> bool:
        return self._enabled


# Singleton instance used across the application
telegram_bot = DurgamTelegramBot()
telegram_police_service = telegram_bot

