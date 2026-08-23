from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from app.database import Base

import datetime


# ============================================================
# USER
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )


# ============================================================
# COST RECORD
# ============================================================

class CostRecord(Base):

    __tablename__ = "cost_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Billing information

    billing_date = Column(
        Date,
        nullable=False,
        index=True
    )

    service = Column(
        String,
        nullable=False,
        index=True
    )

    region = Column(
        String,
        default="Global"
    )

    # Cost information

    amount = Column(
        Float,
        nullable=False
    )

    usage = Column(
        Float,
        default=0.0
    )

    currency = Column(
        String,
        default="USD"
    )

    # Billing metadata

    granularity = Column(
        String,
        default="DAILY"
    )

    billing_period_start = Column(
        Date
    )

    billing_period_end = Column(
        Date
    )

    # User mapping

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Audit fields

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    user = relationship(
        "User"
    )


# ============================================================
# BUDGET
# ============================================================

class Budget(Base):

    __tablename__ = "budgets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount = Column(
        Float
    )

    period = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    user = relationship(
        "User"
    )


# ============================================================
# ANOMALY
# ============================================================

class Anomaly(Base):

    __tablename__ = "anomalies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    date = Column(
        Date,
        index=True
    )

    service = Column(
        String,
        index=True
    )

    detected_on = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    details = Column(
        String
    )

    cost_record_id = Column(
        Integer,
        ForeignKey("cost_records.id")
    )

    # --------------------------------------------------------
    # Explainable anomaly evidence
    # --------------------------------------------------------

    actual_cost = Column(
        Float,
        default=0.0
    )

    expected_cost = Column(
        Float,
        default=0.0
    )

    deviation_percent = Column(
        Float,
        default=0.0
    )

    severity = Column(
        String,
        default="medium"
    )

    detection_method = Column(
        String,
        default="Isolation Forest"
    )

    cost_record = relationship(
        "CostRecord"
    )


# ============================================================
# RECOMMENDATION
# ============================================================

class Recommendation(Base):

    __tablename__ = "recommendations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    service = Column(
        String
    )

    resource_id = Column(
        String
    )

    recommendation = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    user = relationship(
        "User"
    )