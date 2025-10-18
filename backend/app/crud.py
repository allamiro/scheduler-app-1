from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


class SchedulerService:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Doctor methods
    def list_doctors(self) -> List[models.Doctor]:
        return self.session.query(models.Doctor).order_by(models.Doctor.name).all()

    def get_doctor(self, doctor_id: int) -> models.Doctor:
        doctor = self.session.get(models.Doctor, doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor

    def create_doctor(self, doctor_in: schemas.DoctorCreate) -> models.Doctor:
        doctor = models.Doctor(**doctor_in.dict())
        self.session.add(doctor)
        try:
            self.session.commit()
        except IntegrityError as exc:  # unique constraint on name
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A doctor with this name already exists",
            ) from exc
        self.session.refresh(doctor)
        return doctor

    def update_doctor(self, doctor_id: int, doctor_in: schemas.DoctorUpdate) -> models.Doctor:
        doctor = self.get_doctor(doctor_id)
        for key, value in doctor_in.dict(exclude_unset=True).items():
            setattr(doctor, key, value)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A doctor with this name already exists",
            ) from exc
        self.session.refresh(doctor)
        return doctor

    def delete_doctor(self, doctor_id: int) -> None:
        doctor = self.get_doctor(doctor_id)
        self.session.delete(doctor)
        self.session.commit()

    # Schedule methods
    def list_schedules(self) -> List[models.Schedule]:
        return (
            self.session.query(models.Schedule)
            .order_by(models.Schedule.week_start.desc())
            .all()
        )

    def get_schedule(self, schedule_id: int) -> models.Schedule:
        schedule = self.session.get(models.Schedule, schedule_id)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return schedule

    def get_schedule_for_week(self, week_start: date) -> Optional[models.Schedule]:
        return (
            self.session.query(models.Schedule)
            .filter(models.Schedule.week_start == week_start)
            .first()
        )

    def create_schedule(self, schedule_in: schemas.ScheduleCreate) -> models.Schedule:
        schedule = models.Schedule(**schedule_in.dict())
        self.session.add(schedule)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A schedule already exists for this week",
            ) from exc
        self.session.refresh(schedule)
        return schedule

    # Assignment methods
    def list_assignments(self, schedule_id: int) -> List[models.Assignment]:
        schedule = self.get_schedule(schedule_id)
        return (
            self.session.query(models.Assignment)
            .filter(models.Assignment.schedule_id == schedule.id)
            .order_by(models.Assignment.date.asc(), models.Assignment.assignment_type.asc())
            .all()
        )

    def create_assignment(self, schedule_id: int, assignment_in: schemas.AssignmentCreate) -> models.Assignment:
        schedule = self.get_schedule(schedule_id)
        doctor = self.get_doctor(assignment_in.doctor_id)

        # Check doctor capacity for the assignment day
        existing_assignments = (
            self.session.query(models.Assignment)
            .filter(
                models.Assignment.schedule_id == schedule.id,
                models.Assignment.date == assignment_in.date,
                models.Assignment.doctor_id == doctor.id,
            )
            .count()
        )
        if existing_assignments >= doctor.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor capacity reached for this day",
            )

        assignment = models.Assignment(
            schedule_id=schedule.id,
            doctor_id=doctor.id,
            date=assignment_in.date,
            assignment_type=assignment_in.assignment_type,
        )
        self.session.add(assignment)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor already assigned on this day",
            ) from exc
        self.session.refresh(assignment)
        return assignment

    def delete_assignment(self, schedule_id: int, assignment_id: int) -> None:
        schedule = self.get_schedule(schedule_id)
        assignment = (
            self.session.query(models.Assignment)
            .filter(
                models.Assignment.schedule_id == schedule.id,
                models.Assignment.id == assignment_id,
            )
            .first()
        )
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        self.session.delete(assignment)
        self.session.commit()
