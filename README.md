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
<code><pre>uvicorn main:app --reload</pre></code> 

### Access Swagger UI
Visit: http://localhost:8000/docs<br><br>
<img src="Swagger%20UI.png" alt="Swagger UI" width="900" height="400">

## 📊 API Usage

Click on the dropdown on Post /submit_order. Then click on try it out.<br><br>
<img src="Post%20Submit%20Order%20(A).png" alt="Post Submit Order (A).png" width="900" height="400"><br><br>

Then edit the request body using any submit order. One submit order is given below for reference.<br><br>
### 📤 Submit Order (POST /submit_order)
<code><pre>
{
  "symbol": "BTC-USDT",
  "order_type": "limit",
  "side": "sell",
  "price": 26000,
  "quantity": 2.0
}
</pre></code>

### Sell order <br>
JSON for sell order<br><br>
<img src="Post%20Submit%20Order%20(B).png" alt="Post Submit Order (B).png" width="900" height="400"><br><br>

### Response for sell order<br>
Response for sell order<br><br>
<img src="Post%20Submit%20Order%20(B)%20Response.png" alt="Post Submit Order (B) Response.png" width="900" height="400"><br><br>

### Buy order <br>
JSON for buy order<br><br>
<img src="Post%20Submit%20Order%20(C).png" alt="Post Submit Order (C).png" width="900" height="400"><br><br>

### Response for buy order<br>
Response for buy order<br><br>
<img src="Post%20Submit%20Order%20(C)%20Response.png" alt="Post Submit Order (C) Response.png" width="900" height="400"><br><br>  

## 📥 Get BBO Snapshot (GET /order_book/BTC-USDT)

### Get order /order_book <br>
Checking for symbol BTC-USDT<br><br>
<img src="Get%20Order%20Book.png" alt="Get Order.png" width="900" height="400"><br><br>  

### Response for Get order <br>
Gives best bid and best ask <br><br>
<img src="Get%20Order%20Book%20Response.png" alt="Get Order Response.png" width="900" height="400"><br><br>  


## 📡 WebSocket Endpoints

### 1.&nbsp;&nbsp;/ws/trades<br>
Live trade feed (send JSON objects)
<code><pre>ws://127.0.0.1:8000/ws/trades</pre></code>
### 2.&nbsp;&nbsp;/ws/orderbook<br>
Live order book snapshot
<code><pre>ws://127.0.0.1:8000/ws/orderbook</pre></code><br>
### Live Trade Feed
<img src="Live%20Trading.png" alt="Live Trade" width="900" height="400"><br><br>  

## 🗃️ Inspecting the Database
Run this to check if orders/trades are being persisted:
<code><pre>python database.py</pre></code>
