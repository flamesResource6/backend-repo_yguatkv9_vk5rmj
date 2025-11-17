import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import create_document
from schemas import Order

app = FastAPI(title="Photography Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Photography Booking Backend Running"}

@app.get("/test")
def test_database():
    """Simple database availability check"""
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
    }
    try:
        # Lazy import to avoid errors if env not set
        from database import db
        if db is not None:
            status["database"] = "✅ Connected"
            status["collections"] = db.list_collection_names()
    except Exception as e:
        status["database_error"] = str(e)
    return status

# Request model for simple health
class Health(BaseModel):
    ok: bool

@app.get("/health", response_model=Health)
def health():
    return {"ok": True}

@app.post("/api/orders")
def create_order(order: Order):
    """Create a new order document in MongoDB"""
    try:
        inserted_id = create_document("order", order)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
