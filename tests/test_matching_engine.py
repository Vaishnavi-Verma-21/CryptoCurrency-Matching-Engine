import pytest
from engine.order_book import OrderBook
from engine.models import Order
from engine.utils import generate_id, get_timestamp

def make_order(symbol, order_type, side, quantity, price=None):
    return Order(
        order_id=generate_id(),
        symbol=symbol,
        order_type=order_type,
        side=side,
        quantity=quantity,
        price=price,
        timestamp=get_timestamp()
    )

def test_market_order_matching():
    book = OrderBook("BTC-USDT")

    # Add resting limit sell order
    sell_order = make_order("BTC-USDT", "limit", "sell", 2, 30000)
    book.submit_order(sell_order)

    # Submit market buy order
    buy_order = make_order("BTC-USDT", "market", "buy", 1)
    trades = book.submit_order(buy_order)

    assert len(trades) == 1
    assert trades[0].price == 30000
    assert trades[0].quantity == 1

def test_ioc_order():
    book = OrderBook("BTC-USDT")

    # Add resting limit sell order
    book.submit_order(make_order("BTC-USDT", "limit", "sell", 1, 30000))

    # IOC buy order (should fill immediately and cancel any unfilled)
    ioc_order = make_order("BTC-USDT", "ioc", "buy", 1, 30000)
    trades = book.submit_order(ioc_order)

    assert len(trades) == 1
    assert trades[0].quantity == 1

def test_fok_order_full_fill():
    book = OrderBook("BTC-USDT")

    # Add resting sell order
    book.submit_order(make_order("BTC-USDT", "limit", "sell", 1, 30000))

    # FOK order that should be filled completely
    fok_order = make_order("BTC-USDT", "fok", "buy", 1, 30000)
    trades = book.submit_order(fok_order)

    assert len(trades) == 1
    assert trades[0].quantity == 1

def test_fok_order_partial_fill():
    book = OrderBook("BTC-USDT")

    # Only 0.5 BTC available at 30,000
    book.submit_order(make_order("BTC-USDT", "limit", "sell", 0.5, 30000))

    # FOK order requesting 1 BTC — should cancel
    fok_order = make_order("BTC-USDT", "fok", "buy", 1, 30000)
    trades = book.submit_order(fok_order)

    assert len(trades) == 0  # No trade

def test_bbo_correctness():
    book = OrderBook("BTC-USDT")

    book.submit_order(make_order("BTC-USDT", "limit", "buy", 1, 29000))
    book.submit_order(make_order("BTC-USDT", "limit", "buy", 1, 29500))
    book.submit_order(make_order("BTC-USDT", "limit", "sell", 1, 31000))
    book.submit_order(make_order("BTC-USDT", "limit", "sell", 1, 30500))

    bbo = book.get_bbo()

    assert bbo.best_bid == 29500
    assert bbo.best_ask == 30500
