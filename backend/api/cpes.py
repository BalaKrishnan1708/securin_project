from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from database import CPEMessage
from api.deps import get_db

router = APIRouter(prefix="/api/cpes", tags=["CPES"])

@router.get("")
def get_all_cpes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    total = db.query(CPEMessage).count()
    items = db.query(CPEMessage).order_by(CPEMessage.id).offset(offset).limit(limit).all()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": items
    }

@router.get("/search")
def search_cpes(
    cpe_title: Optional[str] = None,
    cpe_22_uri: Optional[str] = None,
    cpe_23_uri: Optional[str] = None,
    deprecation_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CPEMessage)
    
    if cpe_title:
        query = query.filter(CPEMessage.cpe_title.ilike(f"%{cpe_title}%"))
    if cpe_22_uri:
        query = query.filter(CPEMessage.cpe_22_uri.ilike(f"%{cpe_22_uri}%"))
    if cpe_23_uri:
        query = query.filter(CPEMessage.cpe_23_uri.ilike(f"%{cpe_23_uri}%"))
    if deprecation_date:
        query = query.filter(
            or_(
                CPEMessage.cpe_22_deprecation_date < deprecation_date,
                CPEMessage.cpe_23_deprecation_date < deprecation_date
            )
        )
    
    items = query.all()
    return {"data": items}
