# ระบบจองห้องประชุม (meeting-room-booking)

ระบบเว็บจองห้องประชุมภายในองค์กร — FastAPI + React (Vite/TS/Tailwind) + PostgreSQL 16

> เอกสารประกอบ: [`context.md`](context.md) (บริบท/เหตุผล) · [`design.md`](design.md) (แบบเทคนิค) · [`task.md`](task.md) (แผนงาน)

## โครงสร้าง

```
backend/    FastAPI (Python 3.12) + SQLAlchemy + Alembic
frontend/   React 18 + Vite + TypeScript + Tailwind CSS + Vitest
docker-compose.yml   Postgres 16 (dev) — deploy ครบ 3 service ใน Phase 6
.env.example ตัวแปร env ทั้งหมด (คัดลอกเป็น .env ก่อนใช้)
```

## รัน local (สำหรับ dev)

```bash
# 1) คัดลอก env แล้วแก้ค่าตามจริง
cp .env.example .env

# 2) รัน Postgres
docker compose up -d db

# 3) Backend (อยู่ที่ backend/)
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 4) Frontend (อยู่ที่ frontend/)
npm install
npm run dev
```

> README ฉบับ deploy (docker compose up -d --build) จะเพิ่มใน Phase 6

## เกณฑ์เสร็จของโปรเจกต์

ดูที่ [`task.md`](task.md) § เกณฑ์ "เสร็จ" — สรุปสั้น: 30 ผู้ใช้พร้อมกันไม่ซ้อน, กฎ R1–R7 ครบ, อีเมล+ระบบทน SMTP ล่ม, deploy คำสั่งเดียว, UAT ผ่าน
