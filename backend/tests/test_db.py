"""Smoke test การเชื่อมต่อฐานข้อมูล — พิสูจน์ว่า engine + Postgres ใช้งานได้จริง"""
from sqlalchemy import text

from app.db import engine


def test_engine_connects_and_selects_1():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
    assert result == 1
