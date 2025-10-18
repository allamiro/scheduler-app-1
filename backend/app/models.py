from __future__ import annotations

from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    specialty = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False, default=1)

    assignments = relationship("Assignment", back_populates="doctor", cascade="all, delete")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(Date, nullable=False, unique=True, index=True)
    title = Column(String(150), nullable=False)

    assignments = relationship("Assignment", back_populates="schedule", cascade="all, delete")


class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = (
        UniqueConstraint("schedule_id", "date", "doctor_id", name="unique_assignment_per_day"),
    )

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    assignment_type = Column(String(50), nullable=False)

    schedule = relationship("Schedule", back_populates="assignments")
    doctor = relationship("Doctor", back_populates="assignments")
