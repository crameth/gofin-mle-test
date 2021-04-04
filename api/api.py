from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import io
import os

import pandas as pd
import xgboost as xgb

from database import Database

db = Database()

model = xgb.Booster()
model.load_model('/model/xgb.json')

gojek = FastAPI(
    title="Gojek Web Service",
    version="1.0.0"
)

gojek.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Customer(BaseModel):
    customer_id: int
    registration_date: str
    branch_code: str
    outstanding: float
    credit_limit: float
    bill: float
    total_cash_usage: float
    total_retail_usage: float
    remaining_bill: float
    payment_ratio: float
    overlimit_percentage: float
    payment_ratio_3month: float
    payment_ratio_6month: float
    delinquency_score: float
    years_since_card_issuing: float
    total_usage: float
    remaining_bill_per_number_of_cards: float
    remaining_bill_per_limit: float
    total_usage_per_limit: float
    total_3mo_usage_per_limit: float
    total_6mo_usage_per_limit: float
    utilization_3month: float
    utilization_6month: float
    default_flag: bool

@gojek.get("/")
async def read_root() -> dict:
    return "Hello Gojek, wrong page."

# task 1.1
@gojek.get("/customer-info")
async def customer_info(id: int) -> dict:
    return db.customer_info(id)

# task 1.2
@gojek.get("/registration-info")
async def registration_info(start_date: str, end_date: str) -> dict:
    return db.registration_info(start_date, end_date)

# task 2.1
@gojek.get("/analysis/branch-default-rate")
def branch_default_rate():
    return db.branch_default_rate()

# task 2.2
@gojek.get("/analysis/branch-credit-line")
def branch_credit_line():
    return db.branch_credit_line()

# task 2.3
@gojek.get("/analysis/branch-top-default")
def branch_top_default():
    return db.branch_top_default()

# task 3.1
@gojek.post("/model/credit-score")
def credit_score(customer: Customer):
    customer = customer.dict()
    customer_id = customer["customer_id"]

    del customer["customer_id"]
    del customer["registration_date"]
    del customer["branch_code"]
    del customer["bill"]
    del customer["years_since_card_issuing"]
    del customer["default_flag"]

    D_test = pd.DataFrame(customer, index=[0])
    D_test = xgb.DMatrix(D_test)
    preds = model.predict(D_test)

    return {
        "customer_id": customer_id,
        "credit_score": float(preds[0])
    }
