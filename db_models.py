# db_models.py
"""
SQLite + SQLAlchemy models for FairHire AI.
Keeps a summary of each analysed resume for reporting / HR dashboard.
"""

from datetime import datetime
import json

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite DB file (same folder  fairhire.db created)
DATABASE_URL = "sqlite:///fairhire.db"

# Engine (connected DB connection)
engine = create_engine(
    DATABASE_URL,
    echo=False,   # If set True then see the logs 
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

Base = declarative_base()


class Candidate(Base):
    """
    candidates टेबल:
    - candidate_id (UUID)
    - name
    - email
    - domain
    - score
    - selected (True/False)
    - matched / missing skills (JSON string)
    - source: "candidate_portal" / "hr_bulk"
    - created_at
    """
    __tablename__ = "candidates"

    candidate_id = Column(String, primary_key=True, index=True)

    # 🔹 NEW FIELDS
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)

    domain = Column(String, nullable=False)
    score = Column(Float)
    selected = Column(Boolean, default=False)

    matched_skills = Column(Text)     # JSON list
    missing_skills = Column(Text)     # JSON list

    # 🔹 NEW FIELD –ी
    source = Column(String, nullable=True)  # "candidate_portal" / "hr_bulk"

    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def save_candidate_summary(analysis: dict):
    """
    CANDIDATE_ANALYSIS मधल्या analysis dict वरून
    candidates table मध्ये summary insert / update करते.
    """
    from sqlalchemy.exc import SQLAlchemyError

    candidate_id = analysis.get("candidate_id")
    if not candidate_id:
        return

    obj = Candidate(
        candidate_id=candidate_id,
        name=analysis.get("name"),
        email=analysis.get("email"),
        domain=analysis.get("domain") or "unknown",
        score=analysis.get("score"),
        selected=bool(analysis.get("selected")),
        matched_skills=json.dumps(analysis.get("matched_skills", [])),
        missing_skills=json.dumps(analysis.get("missing_skills", [])),
        source=analysis.get("source") or "candidate_portal",
    )

    try:
        with SessionLocal() as session:
            #
            session.merge(obj)
            session.commit()
    except SQLAlchemyError as e:
        print("[DB] Error while saving candidate summary:", e)


def fetch_candidates_with_stats(limit: int = 50):
    """
    Last N candidates + basic stats परत करतो.
    Return: (candidate_rows, stats_dict)
    """
    from sqlalchemy.exc import SQLAlchemyError

    rows = []
    stats = {
        "total": 0,
        "selected": 0,
        "rejected": 0,
        "avg_score": None,
    }

    try:
        with SessionLocal() as session:
            # list of candidates (latest first)
            q = (
                session.query(Candidate)
                .order_by(Candidate.created_at.desc())
                .limit(limit)
            )
            objs = q.all()

            for c in objs:
                rows.append(
                    {
                        "candidate_id": c.candidate_id,
                        "name": c.name,
                        "email": c.email,
                        "domain": c.domain,
                        "score": c.score,
                        "selected": c.selected,
                        "source": c.source,
                        "created_at": c.created_at.isoformat() if c.created_at else None,
                    }
                )

            # stats
            stats["total"] = session.query(func.count(Candidate.candidate_id)).scalar() or 0
            stats["selected"] = (
                session.query(func.count(Candidate.candidate_id))
                .filter(Candidate.selected.is_(True))
                .scalar()
                or 0
            )
            stats["rejected"] = stats["total"] - stats["selected"]
            stats["avg_score"] = (
                session.query(func.avg(Candidate.score)).scalar()
            )

    except SQLAlchemyError as e:
        print("[DB] Error while fetching candidates:", e)

    return rows, stats
