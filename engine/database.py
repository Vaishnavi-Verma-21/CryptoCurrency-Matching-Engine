# engine/database.py

import sqlite3
from .models import Order, Trade
from typing import Any

DB_NAME = "trades.db"

def insert_order(order: Order) -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_id, symbol, order_type, side, quantity, price, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order.order_id,
        order.symbol,
        order.order_type,
        order.side,
        order.quantity,
        order.price,
        order.timestamp.isoformat()
    ))
    conn.commit()
    conn.close()

def insert_trade(trade: Trade) -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (trade_id, symbol, price, quantity, aggressor_side,
                            maker_order_id, taker_order_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trade.trade_id,
        trade.symbol,
        trade.price,
        trade.quantity,
        trade.aggressor_side,
        trade.maker_order_id,
        trade.taker_order_id,
        trade.timestamp.isoformat()
    ))
    conn.commit()
    conn.close()
