from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.record import FinancialRecord
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    active = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == 0)

    total_income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == "income",
        FinancialRecord.is_deleted == 0
    ).scalar() or 0.0

    total_expense = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == "expense",
        FinancialRecord.is_deleted == 0
    ).scalar() or 0.0

    total_records = active.count()

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_balance": round(total_income - total_expense, 2),
        "total_records": total_records
    }


@router.get("/category-breakdown")
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        FinancialRecord.category,
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.is_deleted == 0
    ).group_by(
        FinancialRecord.category,
        FinancialRecord.type
    ).all()

    breakdown = {}
    for category, type_, total in results:
        if category not in breakdown:
            breakdown[category] = {}
        breakdown[category][type_] = round(total, 2)

    return breakdown


@router.get("/monthly-trends")
def get_monthly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        func.strftime("%Y-%m", FinancialRecord.date).label("month"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.is_deleted == 0
    ).group_by("month", FinancialRecord.type).order_by("month").all()

    trends = {}
    for month, type_, total in results:
        if month not in trends:
            trends[month] = {"income": 0.0, "expense": 0.0}
        trends[month][type_] = round(total, 2)

    return trends


@router.get("/recent-activity")
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == 0
    ).order_by(FinancialRecord.created_at.desc()).limit(limit).all()

    return [
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in records
    ]