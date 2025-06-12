# engine/order_book.py

from collections import defaultdict, deque
from typing import List, Dict, Optional
from .models import Order, Trade, BBO
from .utils import generate_id, get_timestamp

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids: Dict[float, deque] = defaultdict(deque)
        self.asks: Dict[float, deque] = defaultdict(deque)
        self.trades: List[Trade] = []

    def get_bbo(self) -> BBO:
        best_bid = max(self.bids.keys(), default=None)
        best_ask = min(self.asks.keys(), default=None)
        return BBO(
            symbol=self.symbol,
            best_bid=best_bid,
            best_ask=best_ask,
            timestamp=get_timestamp()
        )

    def _add_order_to_book(self, order: Order):
        book = self.bids if order.side == "buy" else self.asks
        book[order.price].append(order)

    def _match_order(self, incoming_order: Order) -> List[Trade]:
        trades = []
        book = self.asks if incoming_order.side == "buy" else self.bids
        price_levels = sorted(book.keys(), reverse=(incoming_order.side == "sell"))
        remaining_qty = incoming_order.quantity

        for price in price_levels:
            # Skip limit price check for market orders
            if incoming_order.order_type != "market":
                if (incoming_order.side == "buy" and incoming_order.price < price) or \
                    (incoming_order.side == "sell" and incoming_order.price > price):
                    break


            while book[price] and remaining_qty > 0:
                maker_order = book[price][0]
                trade_qty = min(remaining_qty, maker_order.quantity)
                trade_price = maker_order.price
                trade = Trade(
                    trade_id=generate_id(),
                    symbol=incoming_order.symbol,
                    price=trade_price,
                    quantity=trade_qty,
                    aggressor_side=incoming_order.side,
                    maker_order_id=maker_order.order_id,
                    taker_order_id=incoming_order.order_id,
                    timestamp=get_timestamp()
                )
                trades.append(trade)
                self.trades.append(trade)

                maker_order.quantity -= trade_qty
                remaining_qty -= trade_qty

                if maker_order.quantity == 0:
                    book[price].popleft()
                else:
                    break

            if not book[price]:
                del book[price]

            if remaining_qty == 0:
                break

        return trades

    def submit_order(self, order: Order) -> List[Trade]:
        trades = self._match_order(order)
        if order.order_type == "limit" and order.quantity > 0:
            self._add_order_to_book(order)
        return trades

    # Inside engine/order_book.py
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

