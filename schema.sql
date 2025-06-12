CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    symbol TEXT,
    order_type TEXT,
    side TEXT,
    quantity REAL,
    price REAL,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS trades (
    trade_id TEXT PRIMARY KEY,
    symbol TEXT,
    price REAL,
    quantity REAL,
    aggressor_side TEXT,
    maker_order_id TEXT,
    taker_order_id TEXT,
    timestamp TEXT
);
