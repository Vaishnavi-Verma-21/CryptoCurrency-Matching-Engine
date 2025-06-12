# ws/market_data.py

from fastapi import WebSocket
from typing import List
from starlette.websockets import WebSocketState
import asyncio
from engine.order_book import OrderBook

active_connections: List[WebSocket] = []
order_book = OrderBook("BTC-USDT")

async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)

async def broadcast_order_book():
    if not active_connections:
        return
    bbo = order_book.get_bbo()
    message = {
        "symbol": bbo.symbol,
        "timestamp": bbo.timestamp.isoformat(),
        "best_bid": bbo.best_bid,
        "best_ask": bbo.best_ask
    }
    for connection in active_connections:
        if connection.application_state == WebSocketState.CONNECTED:
            await connection.send_json(message)

async def broadcast_trade_data(trades):
    if not active_connections:
        return
    for trade in trades:
        message = {
            "timestamp": trade.timestamp.isoformat(),
            "symbol": trade.symbol,
            "trade_id": trade.trade_id,
            "price": trade.price,
            "quantity": trade.quantity,
            "aggressor_side": trade.aggressor_side,
            "maker_order_id": trade.maker_order_id,
            "taker_order_id": trade.taker_order_id,
        }
        for connection in active_connections:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_json(message)
