# engine/models.py
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum

class OrderType(str, Enum):
    market = "market"
    limit = "limit"
    ioc = "ioc"
    fok = "fok"


class Order(BaseModel):
    order_id: str
    symbol: str
    order_type: str  # market, limit, ioc, fok
    side: str        # buy or sell
    quantity: float
    price: Optional[float] = None
    timestamp: datetime

class OrderRequest(BaseModel):
    symbol: str
    order_type: OrderType
    side: str
    quantity: float
    price: Optional[float] = None
    
class Trade(BaseModel):
    trade_id: str
    symbol: str
    price: float
    quantity: float
    aggressor_side: str
    maker_order_id: str
    taker_order_id: str
    timestamp: datetime

class BBO(BaseModel):
    symbol: str
    best_bid: Optional[float]
    best_ask: Optional[float]
    timestamp: datetime
