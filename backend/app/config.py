"""ค่า config ทั้งหมดของ backend — อ่านจาก env / .env (ดู .env.example)"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+psycopg://mrb:mrb_dev_password@localhost:5434/meeting_room"

    # Auth
    jwt_secret: str = "change_me_in_production"
    jwt_expire_hours: int = 8

    # Email (ค่าว่าง = ปิดการส่ง, log แทน)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from: str = "meeting-room-booking@example.local"


settings = Settings()
