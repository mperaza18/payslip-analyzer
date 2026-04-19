from typing import Optional
from sqlmodel import Field, SQLModel


class LineItem(SQLModel, table=True):
    __tablename__ = "line_item"

    id: Optional[int] = Field(default=None, primary_key=True)
    payslip_id: str = Field(foreign_key="payslip.uuid_timbre")
    type: str
    code: str
    description: str
    amount: float
