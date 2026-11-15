// Smoke test — พิสูจน์ว่า toolchain (Vitest + TS) รันได้จริง
// ใน Phase ต่อ ๆ ไป จะแทนที่ด้วย test ของกฎ R1–R4 ฝั่ง client และฟอร์มจองซ้ำ
import { describe, expect, it } from 'vitest'

describe('toolchain smoke', () => {
  it('vitest ทำงานและ TS compile ได้', () => {
    const answer: number = 42
    expect(answer).toBe(42)
  })
})
