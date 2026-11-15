# Task — ระบบจองห้องประชุม (meeting-room-booking)

> แผนงานทีละเฟส — งานในเฟสหลังพึ่งเฟสก่อนหน้าเสมอ
> เอกสารประกอบ: `context.md` (ทำไม/ขอบเขต), `design.md` (ทำอย่างไร)

## Phase 0 — เตรียมโครงสร้าง

- [x] สร้างโครง monorepo: `backend/`, `frontend/`, `docker-compose.yml`, `.env.example`, `README.md`
- [x] Backend: ตั้ง Python 3.12 + venv + `requirements.txt` (fastapi, uvicorn, sqlalchemy, alembic, psycopg, passlib[bcrypt], pydantic-settings, pytest)
- [x] Frontend: `npm create vite@latest` (React + TS) + Tailwind CSS + `vitest`
- [x] ตั้ง Postgres 16 ผ่าน Docker (service เดียวพอสำหรับ dev) + ไฟล์ env — host port **5434** (OrbStack ครอง 127.0.0.1:5432 ไว้แล้ว)
- [x] เชื่อม SQLAlchemy + Alembic, รัน migration แรกสำเร็จ

## Phase 1 — Auth และบัญชีผู้ใช้

- [ ] Model `users` + migration
- [ ] `POST /auth/login` — ตรวจ bcrypt, ออก JWT httpOnly cookie (อายุ 8 ชม.), rate limit 10/นาที/IP
- [ ] Dependency `get_current_user` + ตรวจ `is_active`
- [ ] `POST /auth/change-password` + `POST /auth/logout` + `GET /me`
- [ ] Admin: `POST /users` (สร้างบัญชี + รหัสเริ่มต้น + `must_change_password=true`), `PATCH /users/{id}`, `POST /users/{id}/reset-password`
- [ ] **เฟสนี้จบเมื่อ:** ล็อกอินได้, บังคับเปลี่ยนรหัสครั้งแรกทำงาน, admin สร้างบัญชี/รีเซ็ตได้ (ทดสอบผ่าน Swagger ก่อน ยังไม่ต้องมีหน้า UI)

## Phase 2 — ห้องและกติกาการจอง (หัวใจของระบบ)

- [ ] Model `rooms`, `series`, `bookings` + migration
- [ ] `booking_rules.py` — เขียนกฎ R1–R7 เป็นฟังก์ชันบริสุทธิ์ (อินพุต: การจองใหม่ + รายการการจองเดิม → ผลลัพธ์: ผ่าน/รายการ conflict) พร้อม unit test **ก่อน**เขียน API
- [ ] Test กรณีขอบ: ซ้อนกันสนิท, ซ้อนบางส่วน, ห่าง 14:59, ห่าง 15:00, จองยาว 4:00 พอดี, ล่วงหน้า 30 วันพอดี
- [ ] `POST /bookings` — ครั้งเดียว: transaction + `SELECT ... FOR UPDATE` แล้ว INSERT (กัน race)
- [ ] `POST /bookings` — ชุดรายสัปดาห์: แตกเป็นรายวัน, ตรวจแต่ละวัน, ตอบ 409 + รายชื่อวันชน; รับ option `skip_conflicts=true` ให้ข้ามวันชน
- [ ] `GET /bookings?date=`, `GET /bookings/week`, `GET /bookings/mine`, `DELETE /bookings/{id}`, `POST /series/{id}/cancel` — ตรวจสิทธิ์ตาม R6
- [ ] Admin rooms CRUD + `is_active` (R7)
- [ ] **เฟสนี้จบเมื่อ:** pytest ครอบ R1–R7 ผ่านทั้งหมด, จองซ้อนถูกปฏิเสธ, จองซ้ำที่มีวันชนตอบรายชื่อวันชนได้ถูกต้อง

## Phase 3 — Frontend ผู้ใช้ทั่วไป

- [ ] โครง SPA: router, axios/fetch wrapper (ตรวจ 401 → ไป `/login`), layout ไทย
- [ ] หน้า Login + บังคับเปลี่ยนรหัส
- [ ] **ตารางรายวัน**: timeline แนวนอน 08:00–20:00, แถวต่อห้อง (เลือกได้), บล็อกจองคลิกดูรายละเอียด, ช่องว่างคลิกเริ่มจอง, ปุ่ม ‹ › + "วันนี้"
- [ ] **ตารางรายสัปดาห์** (`/week`)
- [ ] Dialog สร้างการจอง: ฟอร์ม + สวิตช์จองซ้ำ + ตรวจสด R1–R4 ฝั่ง client + แสดงรายการวันชนและ checkbox ยกเว้นวัน
- [ ] หน้า "การจองของฉัน" + ปุ่มยกเลิก (แสดงตามสิทธิ์ R6) + ยืนยันก่อนยกเลิก + ยกเลิกทั้งชุด
- [ ] Responsive มือถือ (timeline เลื่อนแนวนอนใน container ตัวเอง)
- [ ] **เฟสนี้จบเมื่อ:** ผู้ใช้จองจริงได้ครบวงจรจากหน้าเว็บ — จอง → เห็นบนตาราง → ยกเลิก

## Phase 4 — อีเมลแจ้งเตือน

- [ ] โมดูล mailer อ่าน env SMTP; ส่งไม่ได้ = log แล้วผ่าน (ไม่ fail การจอง)
- [ ] ส่งเมื่อ: จองสำเร็จ (แต่ละวันของชุด), ยกเลิก, สร้างบัญชี/รีเซ็ตรหัส
- [ ] เทมเพลตอีเมลภาษาไทย (ห้อง, วันเวลาเขต Asia/Bangkok, หัวข้อ, ลิงก์)
- [ ] ทดสอบด้วย MailHog/Mailpit ใน docker-compose (profile แยก ไม่รันใน production)
- [ ] **เฟสนี้จบเมื่อ:** อีเมลถึงกล่อง MailHog ครบทุกเหตุการณ์, และระบบยังจองได้เมื่อปิด SMTP

## Phase 5 — หน้า Admin

- [ ] ป้องกันเส้นทาง `/admin/*` (redirect ถ้าไม่ใช่ admin)
- [ ] จัดการห้อง: CRUD + อุปกรณ์ tags + เปิด/ปิด
- [ ] จัดการผู้ใช้: สร้าง (copy รหัสเริ่มต้น), รีเซ็ตรหัส, เปิด/ปิดบัญชี
- [ ] การจองทั้งหมด: ตาราง + กรองวัน/ห้อง + ยกเลิกแทนคนอื่น
- [ ] **เฟสนี้จบเมื่อ:** admin ทำทุกอย่างจากหน้าเว็บได้โดยไม่แตะโค้ด

## Phase 6 — เก็บงานและ deploy

- [ ] API test ครบ flow: login → จอง → conflict 409 → ยกเลิก → 403 ไม่มีสิทธิ์
- [ ] `docker-compose.yml` ครบ 3 service + `.env.production` + entrypoint รัน `alembic upgrade head`
- [ ] Seed script: สร้าง admin คนแรก + ห้องตัวอย่าง 5 ห้อง (สำหรับ go-live)
- [ ] เช็คความปลอดภัย: ไม่มี plaintext password ใน log, cookie flags ถูก, ทุก mutation ตรวจสิทธิ์ฝั่ง server
- [ ] README: วิธีรัน local + วิธี deploy + ตัวแปร env ทั้งหมด
- [ ] UAT กับผู้ใช้จริง 2–3 คน ก่อนประกาศใช้

## เกณฑ์ "เสร็จ" ของโปรเจกต์

1. ผู้ใช้ 30 คนใช้พร้อมกันได้โดยไม่มีการจองซ้อน (ทดสอบ concurrent แล้ว)
2. กฎ R1–R7 ทำงานถูกต้อง 100% ตาม `design.md` §4
3. ทุกเหตุการณ์สำคัญมีอีเมล + ระบบทำงานต่อได้แม้ SMTP ล่ม
4. Deploy ได้ด้วยคำสั่งเดียว `docker compose up -d --build`
5. UAT ผ่านก่อนเปิดใช้จริง
