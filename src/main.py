import os
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

import analytics
from models import (
    DiscountedSaleTransaction,
    InvalidTransactionError,
    SaleTransaction,
    TaxedSaleTransaction,
)

DATA_PATH = Path(
    os.getenv("DATA_PATH", Path(__file__).parent / "data" / "SuperMarket Analysis.csv")
)

app = FastAPI(
    title="Supermarket Sales API",
    description="Analytics over the Kaggle 'Supermarket Sales' dataset.",
    version="1.0.0",
)


@lru_cache(maxsize=1)
def get_df():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=503, detail=f"Dataset not found at {DATA_PATH}")
    return analytics.load_data(DATA_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/summary")
def get_summary():
    return analytics.summary(get_df())


@app.get("/sales/by-branch")
def get_sales_by_branch():
    return analytics.sales_by_branch(get_df())


@app.get("/sales/top-rated")
def get_top_rated():
    return analytics.rating_by_product_line(get_df())


@app.get("/payments")
def get_payments():
    return analytics.payment_counts(get_df())


@app.get("/pivot")
def get_pivot():
    return analytics.pivot(get_df())


@app.get("/report")
def get_report():
    path = os.path.join(tempfile.gettempdir(), "Supermarket_Sales_Report.xlsx")
    analytics.export_report(get_df(), path)
    return FileResponse(
        path,
        filename="Supermarket_Sales_Report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


class TransactionIn(BaseModel):
    product_line: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    rating: Optional[float] = None
    kind: Literal["base", "discounted", "taxed"] = "base"
    rate: Optional[float] = None  # discount (0-1) or tax rate, depending on kind


@app.post("/transactions/validate")
def validate_transaction(t: TransactionIn):
    try:
        if t.kind == "discounted":
            obj = DiscountedSaleTransaction(
                t.product_line, t.unit_price, t.quantity, t.rate, t.rating
            )
        elif t.kind == "taxed":
            rate = 0.05 if t.rate is None else t.rate
            obj = TaxedSaleTransaction(t.product_line, t.unit_price, t.quantity, rate, t.rating)
        else:
            obj = SaleTransaction(t.product_line, t.unit_price, t.quantity, t.rating)
    except InvalidTransactionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"valid": True, "kind": t.kind, "total": round(obj.calculate_total(), 2)}