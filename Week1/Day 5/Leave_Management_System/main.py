from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal, Leave

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/apply")
def apply_leave(employee: str, start_date: date, days: int, reason: str, db: Session = Depends(get_db)):
    leave = Leave(
        employee=employee,
        start_date=start_date,
        days=days,
        reason=reason,
        status="Pending"
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return {"message": "Leave submitted"}

@app.get("/pending")
def pending_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).filter(Leave.status == "Pending").all()

@app.post("/approve/{leave_id}")
def approve_leave(leave_id: int, manager: str, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    leave.status = "Approved"
    leave.approved_by = manager
    db.commit()
    return {"message": "Approved"}

@app.get("/employee/{employee}")
def employee_leaves(employee: str, db: Session = Depends(get_db)):
    return db.query(Leave).filter(Leave.employee == employee).all()

@app.get("/leave/all")
def all_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).all()
