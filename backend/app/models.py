from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True, index=True)

    # Billing Information
    billing_date = Column(Date, nullable=False, index=True)
    service = Column(String, nullable=False, index=True)
    region = Column(String, default="Global")

    # Cost Information
    amount = Column(Float, nullable=False)
    usage = Column(Float, default=0.0)
    currency = Column(String, default="USD")

    # Billing Metadata
    granularity = Column(String, default="DAILY")
    billing_period_start = Column(Date)
    billing_period_end = Column(Date)

    # User Mapping
    user_id = Column(Integer, ForeignKey("users.id"))

    # Audit Fields
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    user = relationship("User")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    period = Column(String)  # monthly / weekly / yearly
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    service = Column(String)

    detected_on = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    details = Column(String)

    cost_record_id = Column(
        Integer,
        ForeignKey("cost_records.id")
    )

    cost_record = relationship("CostRecord")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    service = Column(String)

    resource_id = Column(String)

    recommendation = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    user = relationship("User")