from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import SchedulerService
from ..database import get_session

router = APIRouter(prefix="/doctors", tags=["doctors"])


def get_service(session: Session = Depends(get_session)) -> SchedulerService:
    return SchedulerService(session)


@router.get("/", response_model=list[schemas.Doctor])
def list_doctors(service: SchedulerService = Depends(get_service)):
    return service.list_doctors()


@router.post("/", response_model=schemas.Doctor, status_code=201)
def create_doctor(doctor: schemas.DoctorCreate, service: SchedulerService = Depends(get_service)):
    return service.create_doctor(doctor)


@router.put("/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(
    doctor_id: int, doctor: schemas.DoctorUpdate, service: SchedulerService = Depends(get_service)
):
    return service.update_doctor(doctor_id, doctor)


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int, service: SchedulerService = Depends(get_service)):
    service.delete_doctor(doctor_id)
    return None
