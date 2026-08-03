import { describe, it, expect } from 'vitest'
import { ev1, ev2 } from './exprEval'

describe('ev1 (1D expression)', () => {
  it('evaluates basic arithmetic', () => {
    expect(ev1('2*x', 3)).toBe(6)
  })

  it('handles exponent notation', () => {
    expect(ev1('x^2', 4)).toBe(16)
  })

  it('evaluates trig functions', () => {
    expect(ev1('sin(0)')).toBeCloseTo(0)
    expect(ev1('cos(0)')).toBeCloseTo(1)
  })

  it('handles pi and e', () => {
    expect(ev1('pi')).toBeCloseTo(Math.PI)
    expect(ev1('e')).toBeCloseTo(Math.E)
  })

  it('handles sqrt', () => {
    expect(ev1('sqrt(9)')).toBeCloseTo(3)
  })
})

describe('ev2 (2D expression)', () => {
  it('evaluates multi-variable', () => {
    expect(ev2('x+y', 2, 3)).toBe(5)
  })

  it('handles x*y', () => {
    expect(ev2('x*y', 4, 5)).toBe(20)
  })

  it('handles x^2 + y^2', () => {
    expect(ev2('x^2 + y^2', 3, 4)).toBe(25)
  })
})
