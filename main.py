from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import Base, engine, SessionLocal
from models import ChargingSession

app = FastAPI(title="VoltEdge API")

Base.metadata.create_all(bind=engine)


class ChargingSessionCreate(BaseModel):
    charger_id: str
    user_id: str
    energy_kwh: float
    status: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {
        "status": "running",
        "service": "VoltEdge API"
    }


@app.post("/charging-sessions")
def create_session(
    session_data: ChargingSessionCreate,
    db: Session = Depends(get_db)
):
    session = ChargingSession(
        charger_id=session_data.charger_id,
        user_id=session_data.user_id,
        energy_kwh=session_data.energy_kwh,
        status=session_data.status
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "id": session.id,
        "message": "Charging session saved"
    }


@app.get("/charging-sessions")
def get_sessions(
    db: Session = Depends(get_db)
):
    return db.query(ChargingSession).all()


@app.get("/charging-sessions/{session_id}")
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    return db.query(
        ChargingSession
    ).filter(
        ChargingSession.id == session_id
    ).first()


@app.put("/charging-sessions/{session_id}")
def update_session(
    session_id: int,
    session_data: ChargingSessionCreate,
    db: Session = Depends(get_db)
):
    session = db.query(
        ChargingSession
    ).filter(
        ChargingSession.id == session_id
    ).first()

    if not session:
        return {
            "message": "Session not found"
        }

    session.charger_id = session_data.charger_id
    session.user_id = session_data.user_id
    session.energy_kwh = session_data.energy_kwh
    session.status = session_data.status

    db.commit()
    db.refresh(session)

    return {
        "message": "Session updated",
        "id": session.id
    }


@app.delete("/charging-sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = db.query(
        ChargingSession
    ).filter(
        ChargingSession.id == session_id
    ).first()

    if not session:
        return {
            "message": "Session not found"
        }

    db.delete(session)
    db.commit()

    return {
        "message": "Session deleted"
    }


@app.get("/analytics/total-energy")
def total_energy(
    db: Session = Depends(get_db)
):
    total = db.query(
        func.sum(
            ChargingSession.energy_kwh
        )
    ).scalar()

    return {
        "total_energy_kwh": total or 0
    }