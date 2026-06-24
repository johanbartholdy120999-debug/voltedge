from datetime import date, datetime, time
from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import (
    Kunde,
    Elbil,
    Ladestation,
    Ladepunkt,
    Tarif,
    Opladning,
    Servicehaendelse,
    Driftstilstand,
)

app = FastAPI(title="VoltEdge API")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class KundeCreate(BaseModel):
    navn: str
    email: str
    telefon: Optional[str] = None
    medlemskabstype: Optional[str] = None


class ElbilCreate(BaseModel):
    kunde_id: int
    maerke: Optional[str] = None
    model: Optional[str] = None
    batterikapacitet_kwh: Optional[float] = None
    produktionsaar: Optional[int] = None


class LadestationCreate(BaseModel):
    navn: str
    by: Optional[str] = None
    adresse: Optional[str] = None
    breddegrad: Optional[float] = None
    laengdegrad: Optional[float] = None


class LadepunktCreate(BaseModel):
    ladestation_id: int
    ladetype: Optional[str] = None
    maks_effekt_kw: Optional[float] = None
    installationsdato: Optional[date] = None
    status: Optional[str] = None


class TarifCreate(BaseModel):
    ladestation_id: int
    navn: Optional[str] = None
    tariftype: Optional[str] = None
    pris_per_kwh: Optional[float] = None
    start_tid: Optional[time] = None
    slut_tid: Optional[time] = None


class OpladningCreate(BaseModel):
    kunde_id: int
    elbil_id: int
    ladepunkt_id: int
    tarif_id: int
    energi_kwh: float
    varighed_minutter: Optional[int] = None
    temperatur_c: Optional[float] = None
    pris_per_kwh: Optional[float] = None
    samlet_pris: Optional[float] = None
    starttid: Optional[datetime] = None
    sluttid: Optional[datetime] = None
    status: Optional[str] = None


class ServicehaendelseCreate(BaseModel):
    ladepunkt_id: int
    servicetype: Optional[str] = None
    aarsag: Optional[str] = None
    service_dato: Optional[datetime] = None
    nedetid_timer: Optional[float] = None
    beskrivelse: Optional[str] = None


class DriftstilstandCreate(BaseModel):
    ladepunkt_id: int
    driftsscore: Optional[float] = None
    temperatur_c: Optional[float] = None
    spaending_v: Optional[float] = None
    stroem_a: Optional[float] = None
    fejl_antal: Optional[int] = None
    oppetid_procent: Optional[float] = None
    maaletidspunkt: Optional[datetime] = None


@app.get("/")
def health():
    return {
        "status": "running",
        "service": "VoltEdge API"
    }


@app.post("/kunder")
def create_kunde(kunde: KundeCreate, db: Session = Depends(get_db)):
    item = Kunde(**kunde.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/kunder")
def get_kunder(db: Session = Depends(get_db)):
    return db.query(Kunde).all()


@app.post("/elbiler")
def create_elbil(elbil: ElbilCreate, db: Session = Depends(get_db)):
    item = Elbil(**elbil.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/elbiler")
def get_elbiler(db: Session = Depends(get_db)):
    return db.query(Elbil).all()


@app.post("/ladestationer")
def create_ladestation(ladestation: LadestationCreate, db: Session = Depends(get_db)):
    item = Ladestation(**ladestation.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/ladestationer")
def get_ladestationer(db: Session = Depends(get_db)):
    return db.query(Ladestation).all()


@app.post("/ladepunkter")
def create_ladepunkt(ladepunkt: LadepunktCreate, db: Session = Depends(get_db)):
    item = Ladepunkt(**ladepunkt.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/ladepunkter")
def get_ladepunkter(db: Session = Depends(get_db)):
    return db.query(Ladepunkt).all()


@app.post("/tariffer")
def create_tarif(tarif: TarifCreate, db: Session = Depends(get_db)):
    item = Tarif(**tarif.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/tariffer")
def get_tariffer(db: Session = Depends(get_db)):
    return db.query(Tarif).all()


@app.post("/opladninger")
def create_opladning(opladning: OpladningCreate, db: Session = Depends(get_db)):
    item = Opladning(**opladning.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/opladninger")
def get_opladninger(db: Session = Depends(get_db)):
    return db.query(Opladning).all()


@app.post("/servicehaendelser")
def create_servicehaendelse(
    servicehaendelse: ServicehaendelseCreate,
    db: Session = Depends(get_db)
):
    item = Servicehaendelse(**servicehaendelse.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/servicehaendelser")
def get_servicehaendelser(db: Session = Depends(get_db)):
    return db.query(Servicehaendelse).all()


@app.post("/driftstilstande")
def create_driftstilstand(
    driftstilstand: DriftstilstandCreate,
    db: Session = Depends(get_db)
):
    item = Driftstilstand(**driftstilstand.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/driftstilstande")
def get_driftstilstande(db: Session = Depends(get_db)):
    return db.query(Driftstilstand).all()