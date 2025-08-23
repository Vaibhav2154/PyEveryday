# ⚙️ PyEveryday Web Integration Guide (Next.js + FastAPI)

This guide explains how to set up a full-stack web interface for your **PyEveryday** project using a **Next.js frontend** and **FastAPI backend**. Users will be able to interact with your Python scripts through a clean UI — no need to clone or run anything locally.

---

## 🏗 Architecture Overview

```
[ Next.js Frontend ] ⇄ [ FastAPI Backend ] ⇄ [ Python Scripts ]
```

---

## 📁 Suggested Project Structure

```
pyeveryday-web/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── utilities.py
│   │   └── ...
│   ├── scripts/              # Your existing scripts, refactored as functions
│   └── requirements.txt
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx
│   │   └── utilities/
│   │       └── currency-converter.tsx
│   └── utils/api.ts
```

---

## 🔧 Backend Setup (FastAPI)

### 1. Create virtual environment and install FastAPI:

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install fastapi uvicorn
```

### 2. Refactor a script into a function

**scripts/currency_converter.py**
```python
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    # Your logic here
    return round(amount * 83.2, 2)  # Dummy conversion
```

### 3. Add a router endpoint

**routers/utilities.py**
```python
from fastapi import APIRouter
from scripts.currency_converter import convert_currency

router = APIRouter()

@router.get("/currency-converter")
def currency_converter(amount: float, from_currency: str, to_currency: str):
    result = convert_currency(amount, from_currency, to_currency)
    return {"converted_amount": result}
```

### 4. Set up main FastAPI app

**main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import utilities

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utilities.router, prefix="/utilities")
```

### 5. Run the server

```bash
uvicorn main:app --reload --port 8000
```

---

## 🎨 Frontend Setup (Next.js)

### 1. Create Next.js project

```bash
npx create-next-app@latest frontend
cd frontend
npm install
```

### 2. Create UI to call backend

**pages/utilities/currency-converter.tsx**
```tsx
import { useState } from "react"

export default function CurrencyConverter() {
  const [amount, setAmount] = useState("")
  const [from, setFrom] = useState("USD")
  const [to, setTo] = useState("INR")
  const [result, setResult] = useState("")

  const convert = async () => {
    const res = await fetch(
      \`http://localhost:8000/utilities/currency-converter?amount=\${amount}&from_currency=\${from}&to_currency=\${to}\`
    )
    const data = await res.json()
    setResult(data.converted_amount)
  }

  return (
    <div>
      <h1>Currency Converter</h1>
      <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
      <input value={from} onChange={(e) => setFrom(e.target.value)} />
      <input value={to} onChange={(e) => setTo(e.target.value)} />
      <button onClick={convert}>Convert</button>
      {result && <p>Result: {result}</p>}
    </div>
  )
}
```

---

## 🚀 Run Everything

- **Backend** (from `backend/`):
  ```bash
  uvicorn main:app --reload --port 8000
  ```

- **Frontend** (from `frontend/`):
  ```bash
  npm run dev
  ```

Visit `http://localhost:3000/utilities/currency-converter` to try it!

---

## 🛡 Tips

- Use **Pydantic** in FastAPI for input validation
- Use **Tailwind or Chakra UI** in Next.js for a nice UI
- Use `dotenv` for secrets and environment configs
- Deploy backend with **Render, Railway or Fly.io**
- Deploy frontend with **Vercel** or **Netlify**

---

## 🤝 Contribution Ideas

- Add UI for all PyEveryday scripts
- Convert scripts to support both CLI and API calls
- Add user history tracking (optional DB)
- Add script explorer page

---

Happy Hacking! ⚙️🚀
