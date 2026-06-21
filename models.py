from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class ChargingSession(Base):
    __tablename__ = "charging_sessions"

    id = Column(Integer, primary_key=True, index=True)

    charger_id = Column(String, nullable=False)

    user_id = Column(String, nullable=False)

    energy_kwh = Column(Float, nullable=False)

    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)