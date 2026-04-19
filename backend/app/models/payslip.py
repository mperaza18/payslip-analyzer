from datetime import date, datetime
from sqlmodel import Field, SQLModel


class Payslip(SQLModel, table=True):
    uuid_timbre: str = Field(primary_key=True)
    employee_name: str
    period_start: date
    period_end: date
    total_perceptions: float
    total_deductions: float
    net_pay: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
