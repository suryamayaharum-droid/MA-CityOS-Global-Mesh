"""HoloOS Communication Hub - HTTP, WebSocket, Events"""
from typing import Dict, List, Callable
from dataclasses import dataclass
from enum import Enum
import time

class Protocol(Enum):
    HTTP = "http"
    WEBSOCKET = "websocket"
    EVENT = "event"

@dataclass
class Message:
    id: str
    sender: str
    receiver: str
    content: str
    protocol: Protocol
    timestamp: float

class EventBus:
    """Barramento de eventos"""
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.events: List[Dict] = []
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def publish(self, event_type: str, data: any) -> None:
        event = {"type": event_type, "data": data, "time": time.time()}
        self.events.append(event)
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)

class CommunicationHub:
    """Hub de comunicação unificado"""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.http_routes: Dict[str, Callable] = {}
        self.websocket_connections: List[str] = []
        self.message_history: List[Message] = []
    
    def add_http_route(self, path: str, handler: Callable) -> None:
        self.http_routes[path] = handler
    
    def send_message(self, sender: str, receiver: str, content: str, protocol: Protocol = Protocol.HTTP) -> str:
        msg = Message(
            id=f"msg_{len(self.message_history)}",
            sender=sender,
            receiver=receiver,
            content=content,
            protocol=protocol,
            timestamp=time.time()
        )
        self.message_history.append(msg)
        return msg.id
    
    def broadcast_event(self, event_type: str, data: any) -> None:
        self.event_bus.publish(event_type, data)
    
    def get_status(self) -> Dict:
        return {
            "http_routes": len(self.http_routes),
            "ws_connections": len(self.websocket_connections),
            "events": len(self.events),
            "messages": len(self.message_history),
        }

__all__ = ["CommunicationHub", "EventBus", "Protocol", "Message"]
