from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio
import time
import random

router = APIRouter(tags=["Live Telemetry WebSockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/ws/telemetry")
async def websocket_telemetry_stream(websocket: WebSocket):
    """
    Real-Time WebSocket Stream for Live National Risk-Grid Telemetry.
    Broadcasts simulated live 1930 incident feeds, micro-holds, and patrol dispatches.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Send live heartbeat and simulated live events every 6 seconds
            await asyncio.sleep(6)
            mock_event = {
                "event_type": "LIVE_TELEMETRY_PULSE",
                "timestamp": time.time(),
                "active_hold_count": random.randint(120, 145),
                "funds_protected_total_cr": round(random.uniform(42.5, 48.9), 2),
                "live_incident_alert": {
                    "case_id": f"DURGAM-PULSE-{random.randint(100, 999)}",
                    "origin": random.choice(["Delhi", "Mumbai", "Bengaluru", "Kolkata"]),
                    "terminal_destination": random.choice(["Jammu", "Nuh", "Jamtara", "Jaipur"]),
                    "amount": random.choice([50000, 100000, 250000, 500000]),
                    "status": "MICRO_HOLD_QUARANTINED"
                }
            }
            await websocket.send_json(mock_event)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
