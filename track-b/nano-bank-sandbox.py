from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from faker import Faker

# --- 1. DATA MODELS & SQLITE SETUP ---
class Account(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner: str
    balance: int = 100000  # USD starting balance

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: str
    type: str  # "DEPOSIT" or "WITHDRAWAL"
    amount: int
    merchant: str
    date: str  # "YYYY-MM-DD"

class AmountRequest(SQLModel):
    amount: int

engine = create_engine("sqlite:///nano_bank.db", connect_args={"check_same_thread": False})[cite: 8]
SQLModel.metadata.create_all(engine)[cite: 8]

# --- 2. SEED SYNTHETIC DATA (Runs once on startup) ---
with Session(engine) as session:
    if not session.get(Account, "ACC101"):
        session.add(Account(id="ACC101", owner="Alice"))[cite: 8]
        fake = Faker()
        for month in range(1, 13):
            month_str = f"2025-{month:02d}"
            session.add(Transaction(account_id="ACC101", type="DEPOSIT", amount=5000, merchant="Salary", date=f"{month_str}-01"))[cite: 8]
            session.add(Transaction(account_id="ACC101", type="WITHDRAWAL", amount=180, merchant=fake.company(), date=f"{month_str}-15"))[cite: 8]
        session.commit()[cite: 8]

app = FastAPI(title="Nano Bank Sandbox")[cite: 8]

# --- 3. CORE BANKING APIS ---
@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, req: AmountRequest):
    if req.amount <= 0:
        raise HTTPException(400, "Amount must be positive")
    with Session(engine) as session:
        acc = session.get(Account, account_id)
        if not acc:
            raise HTTPException(404, "Account not found")[cite: 8]
        acc.balance += req.amount
        session.add(Transaction(account_id=account_id, type="DEPOSIT", amount=req.amount, merchant="Deposit", date="2026-11-06"))[cite: 8]
        session.commit()[cite: 8]
        return {"account_id": acc.id, "balance": acc.balance}[cite: 8]

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, req: AmountRequest):
    if req.amount <= 0:
        raise HTTPException(400, "Amount must be positive")
    with Session(engine) as session:
        acc = session.get(Account, account_id)
        if not acc:
            raise HTTPException(404, "Account not found")[cite: 8]
        if req.amount > acc.balance:
            raise HTTPException(409, "Insufficient funds")[cite: 8]
        acc.balance -= req.amount
        session.add(Transaction(account_id=account_id, type="WITHDRAWAL", amount=req.amount, merchant="Withdrawal", date="2026-11-06"))[cite: 8]
        session.commit()[cite: 8]
        return {"account_id": acc.id, "balance": acc.balance}[cite: 8]

@app.get("/accounts/{account_id}/statement/{year}/{month}")
def get_statement(account_id: str, year: int, month: int):
    with Session(engine) as session:
        acc = session.get(Account, account_id)
        if not acc:
            raise HTTPException(404, "Account not found")[cite: 8]
        
        target_prefix = f"{year}-{month:02d}"
        all_txs = session.exec(select(Transaction).where(Transaction.account_id == account_id)).all()[cite: 8]
        month_txs = [t for t in all_txs if t.date.startswith(target_prefix)][cite: 8]
        
        deposits = sum(t.amount for t in month_txs if t.type == "DEPOSIT")[cite: 8]
        withdrawals = sum(t.amount for t in month_txs if t.type == "WITHDRAWAL")[cite: 8]
        
        return {
            "account_id": account_id,
            "month": target_prefix,
            "total_deposits": deposits,
            "total_withdrawals": withdrawals,
            "net_flow": deposits - withdrawals,
            "current_balance": acc.balance,
            "transactions": month_txs
        }

# --- 4. AI EXTENSION SLOTS (To be filled in during modules) ---
@app.post("/ai/chat")
def ai_chat(prompt: str):
    """Module 1: Direct LLM Chat via LiteLLM"""
    return {"answer": "TODO: Implement direct chat in Module 1"}

@app.post("/ai/rag")
def ai_rag(question: str):
    """Module 2: Policy & Statement RAG via LlamaIndex"""
    return {"answer": "TODO: Implement vector retrieval in Module 2"}

@app.post("/ai/agent")
def ai_agent(query: str):
    """Module 3: Database Tool Calling / Text-to-SQL"""
    return {"answer": "TODO: Implement function calling in Module 3"}