# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine.models import OrderRequest, Order, Trade
from engine.order_book import OrderBook
from engine.utils import generate_id, get_timestamp
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single instance of the order book for "BTC-USDT"
order_book = OrderBook("BTC-USDT")

# Store connected clients
connected_trade_clients = []
connected_orderbook_clients = set()

# --- WebSocket Endpoints ---

@app.websocket("/ws/trades")
async def trade_stream(websocket: WebSocket):
    await websocket.accept()
    connected_trade_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        connected_trade_clients.remove(websocket)

@app.websocket("/ws/orderbook")
async def websocket_orderbook(websocket: WebSocket):
    await websocket.accept()
    connected_orderbook_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connected_orderbook_clients.remove(websocket)

# --- Broadcast Functions ---

async def broadcast_trade_data(trades: list[Trade]):
    if not trades:
        return
    for client in connected_trade_clients:
        for trade in trades:
            print("Broadcasting trade to clients:", trade.model_dump())
            await client.send_json({
                "type": "trade",
                "data": trade.model_dump(mode="json") 
            })
async def broadcast_orderbook_update(snapshot: dict):
    print("Broadcasting snapshot to clients:", snapshot) 
    disconnected = set()
    for ws in connected_orderbook_clients:
        try:
            await ws.send_json(snapshot)
        except:
            disconnected.add(ws)
    connected_orderbook_clients.difference_update(disconnected)

# --- Order Submission Endpoint ---

@app.post("/submit_order")
async def submit_order(order_req: OrderRequest):
    new_order = Order(
        order_id=generate_id(),
        symbol=order_req.symbol,
        order_type=order_req.order_type,
        side=order_req.side,
        quantity=order_req.quantity,
        price=order_req.price,
        timestamp=get_timestamp()
    )

    trades = order_book.submit_order(new_order)

    # Broadcast updates
    print("🔹 New Order Submitted:", new_order.dict())
    print("🔹 Trades Generated:", trades)
    await broadcast_trade_data(trades)
    snapshot = order_book.get_order_book_snapshot()
    print("🔹 Broadcasting Orderbook Snapshot:", snapshot)
    await broadcast_orderbook_update(snapshot)

    return {
        "message": "Order submitted successfully",
        "order_id": new_order.order_id,
        "trades": [t.dict() for t in trades]
    }

# --- REST: Get current BBO ---
@app.get("/order_book/{symbol}")
def get_order_book(symbol: str):
    bbo = order_book.get_bbo()
    return {
        "timestamp": bbo.timestamp,
        "symbol": bbo.symbol,
        "best_bid": bbo.best_bid,
        "best_ask": bbo.best_ask
    }
def get_order_book_snapshot(self) -> dict:
    return {
        "symbol": self.symbol,
        "asks": [
            [str(price), sum(order.quantity for order in orders)]
            for price, orders in sorted(self.asks.items())
        ],
        "bids": [
            [str(price), sum(order.quantity for order in orders)]
            for price, orders in sorted(self.bids.items(), reverse=True)
        ],
        "timestamp": get_timestamp()
    }


