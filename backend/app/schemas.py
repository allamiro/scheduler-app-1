from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class DoctorBase(BaseModel):
    name: str = Field(..., max_length=100)
    specialty: str = Field(..., max_length=100)
    capacity: int = Field(ge=1)


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    specialty: Optional[str] = Field(None, max_length=100)
    capacity: Optional[int] = Field(None, ge=1)


class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class AssignmentBase(BaseModel):
    date: date
    assignment_type: str = Field(..., max_length=50)


class AssignmentCreate(AssignmentBase):
    doctor_id: int


class Assignment(AssignmentBase):
    id: int
    doctor: Doctor

    class Config:
        orm_mode = True


class ScheduleBase(BaseModel):
    week_start: date
    title: str


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int
    assignments: List[Assignment]

    class Config:
        orm_mode = True
