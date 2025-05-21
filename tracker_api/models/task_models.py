from pydantic import BaseModel, validator
from datetime import date

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    due_date: date
    status: str

    @validator("due_date")
    def validate_due_date(cls, v):
        if v < date.today():
            raise ValueError("due_date must be today or in the future")
        return v

    @validator("status")
    def validate_status(cls, v):
        allowed = {"pending", "in_progress", "done"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v