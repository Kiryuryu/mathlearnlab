// Math expression evaluation — translate user input into JS and evaluate safely.

const REPLACE_RULES = [
  [/\^/g, '**'],
  [/sin\(/g, 'Math.sin('],
  [/cos\(/g, 'Math.cos('],
  [/tan\(/g, 'Math.tan('],
  [/exp\(/g, 'Math.exp('],
  [/log\(/g, 'Math.log('],
  [/sqrt\(/g, 'Math.sqrt('],
  [/abs\(/g, 'Math.abs('],
  [/pi/gi, 'Math.PI'],
]

function translate(expr) {
  let s = String(expr)
  for (const [re, to] of REPLACE_RULES) s = s.replace(re, to)
  s = s.replace(/\be\b/gi, 'Math.E')
  return s
}

export function ev1(expr, x) {
  const s = translate(expr)
  return Function('x', 'return ' + s)(x)
}

export function ev2(expr, x, y) {
  const s = translate(expr)
  return Function('x', 'y', 'return ' + s)(x, y)
}
