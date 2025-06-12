# ⚡ Cryptocurrency Matching Engine

A high-performance cryptocurrency matching engine inspired by **REG NMS principles**, built with **FastAPI** (Python), supporting multiple order types (limit, market, IOC, FOK), WebSocket trade feeds, and a persistent SQLite database.

---

## 📌 Project Overview

This engine simulates how crypto exchanges operate, by:

- Matching incoming buy/sell orders based on price-time priority.
- Supporting **limit**, **market**, **IOC**, and **FOK** order types.
- Streaming live trades and order book snapshots via **WebSocket**.
- Persisting orders and trades in an **SQLite** database.
- Serving REST endpoints to submit orders and fetch BBO (Best Bid & Offer).

---

## 🚀 Features

### ✅ Core Functionalities

- **Submit Orders:** `/submit_order` endpoint (REST API).
- **Order Matching:** Implements price-time priority matching engine.
- **Live Feeds:** WebSocket endpoints for real-time trade and book updates.
- **Database Persistence:** Orders and trades stored in SQLite.
- **REST API:** `/order_book/{symbol}` returns latest BBO snapshot.

### 🔁 Order Types

| Type     | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| Limit    | Executes at a specified price or better. Remains in book if not filled.     |
| Market   | Executes immediately at best available price. Requires opposite liquidity.  |
| IOC      | Immediate-Or-Cancel. Fills what it can instantly, cancels rest.             |
| FOK      | Fill-Or-Kill. Executes only if the entire quantity can be filled at once.   |

---

## 🧠 REG NMS Inspiration

This engine mimics **price-time priority** order matching—core to REG NMS regulation used in U.S. stock markets:
- Orders are matched based on **best price**, then by **earliest time**.
- Ensures fairness and transparency in the execution process.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** – web server and WebSocket support
- **SQLite** – lightweight database for persistent storage
- **Pydantic** – data validation and serialization
- **Uvicorn** – ASGI server for FastAPI
- **WebSockets** – live feed for order book and trade stream

---

## 📂 Project Structure

├── main.py # FastAPI app with REST + WebSocket endpoints <br>
├── engine/ <br>
│ ├── models.py # Data models for Order, Trade, BBO <br>
│ ├── order_book.py # Matching engine logic <br>
│ ├── utils.py # Helpers (UUIDs, timestamps) <br>
├── database.py # Database persistence layer <br>
├── orders.db # SQLite DB (auto-created) <br>
└── README.md # This file <br>


---

## 🔧 Getting Started

### Cloning the Repository
<pre> <code>git clone https://github.com/Vaishnavi-Verma-21/CryptoCurrency-Matching-Engine.git </code> </pre>
### Navigate to the project directory:
<pre> <code>cd CryptoCurrency-Matching-Engine </code> </pre>

### Creating Virtual Environment
<pre><code>python -m venv venv </code> </pre>
### Activating Virtual Environment
<pre><code>source venv/bin/activate </code> </pre>
### Installation
Install the project dependencies<code><pre>pip install fastapi uvicorn websockets pydantic</code> </pre>

### Run the App
<code><pre>uvicorn main:app --reload</code> </pre>

### Access Swagger UI
Visit: http://localhost:8000/docs

## 📡 WebSocket Endpoints
<strong>Endpoint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Description</strong><br>
/ws/trades&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Live trade feed (send JSON objects)<br>
/ws/orderbook&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Live order book snapshot<br>

## 📊 API Usage
### 📤 Submit Order (POST /submit_order)
<code><pre>
{
  "symbol": "BTC-USDT",
  "order_type": "limit",
  "side": "buy",
  "price": 26000,
  "quantity": 1.0
}
</pre></code>
### 📥 Get BBO Snapshot (GET /order_book/BTC-USDT)
Returns best bid & ask for the pair.

## 🗃️ Inspecting the Database
Run this to check if orders/trades are being persisted:

<code><pre>python database.py</pre></code>
