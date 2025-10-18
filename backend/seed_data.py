from __future__ import annotations

from datetime import date, timedelta

from app import models
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)


def seed() -> None:
    session = SessionLocal()
    try:
        if session.query(models.Doctor).count() > 0:
            print("Database already seeded")
            return

        doctors = [
            models.Doctor(name="Dr. Alice Johnson", specialty="MRI", capacity=2),
            models.Doctor(name="Dr. Ben Smith", specialty="CT", capacity=1),
            models.Doctor(name="Dr. Carla Espinoza", specialty="Ultrasound", capacity=1),
        ]
        session.add_all(doctors)
        session.flush()

        week_start = date.today() - timedelta(days=date.today().weekday())
        schedule = models.Schedule(title="Radiology Coverage", week_start=week_start)
        session.add(schedule)
        session.flush()

        assignments = [
            models.Assignment(
                schedule_id=schedule.id,
                doctor_id=doctors[0].id,
                date=week_start,
                assignment_type="Morning",
            ),
            models.Assignment(
                schedule_id=schedule.id,
                doctor_id=doctors[1].id,
                date=week_start + timedelta(days=1),
                assignment_type="Evening",
            ),
        ]
        session.add_all(assignments)
        session.commit()
        print("Seed data created")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
