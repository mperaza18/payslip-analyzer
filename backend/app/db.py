from sqlmodel import SQLModel, create_engine, Session, text
from .config import settings
from .models import Payslip, LineItem  # noqa: F401 — registers SQLModel metadata

engine = create_engine(settings.DATABASE_URL, echo=False)

_PERIODS_VIEW_SQL = """\
CREATE VIEW IF NOT EXISTS periods AS
SELECT strftime('%Y', period_start) AS year,
       strftime('%m', period_start) AS month,
       COUNT(*)                     AS payslip_count,
       SUM(total_perceptions)       AS total_perceptions,
       SUM(total_deductions)        AS total_deductions,
       SUM(net_pay)                 AS net_pay
FROM payslip
GROUP BY year, month
"""


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text(_PERIODS_VIEW_SQL))
        conn.commit()


def get_session():
    with Session(engine) as session:
        yield session
