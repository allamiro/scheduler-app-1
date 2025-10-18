from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import SchedulerService
from ..database import get_session

router = APIRouter(prefix="/schedules", tags=["schedules"])


def get_service(session: Session = Depends(get_session)) -> SchedulerService:
    return SchedulerService(session)


@router.get("/", response_model=list[schemas.Schedule])
def list_schedules(service: SchedulerService = Depends(get_service)):
    return service.list_schedules()


@router.post("/", response_model=schemas.Schedule, status_code=201)
def create_schedule(
    schedule: schemas.ScheduleCreate, service: SchedulerService = Depends(get_service)
):
    return service.create_schedule(schedule)


@router.get("/week/{week_start}", response_model=schemas.Schedule | None)
def get_schedule_for_week(week_start: date, service: SchedulerService = Depends(get_service)):
    return service.get_schedule_for_week(week_start)


@router.get("/{schedule_id}/assignments", response_model=list[schemas.Assignment])
def list_assignments(schedule_id: int, service: SchedulerService = Depends(get_service)):
    return service.list_assignments(schedule_id)


@router.post("/{schedule_id}/assignments", response_model=schemas.Assignment, status_code=201)
def create_assignment(
    schedule_id: int,
    assignment: schemas.AssignmentCreate,
    service: SchedulerService = Depends(get_service),
):
    return service.create_assignment(schedule_id, assignment)


@router.delete("/{schedule_id}/assignments/{assignment_id}", status_code=204)
def delete_assignment(
    schedule_id: int, assignment_id: int, service: SchedulerService = Depends(get_service)
):
    service.delete_assignment(schedule_id, assignment_id)
    return None
