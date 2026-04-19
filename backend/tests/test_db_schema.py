import pytest
from sqlmodel import create_engine, text
import app.db as db_module


@pytest.fixture()
def patched_db(tmp_path, monkeypatch):
    test_engine = create_engine(f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setattr(db_module, "engine", test_engine)
    yield test_engine


def test_payslip_table_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='payslip'")
        ).first()
    assert row is not None, "payslip table should exist after init_db()"


def test_line_item_table_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='line_item'")
        ).first()
    assert row is not None, "line_item table should exist after init_db()"


def test_periods_view_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='view' AND name='periods'")
        ).first()
    assert row is not None, "periods view should exist after init_db()"
