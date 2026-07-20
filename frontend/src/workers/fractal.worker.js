self.onmessage = function(e) {
  const { mode, width, height, cx, cy, range, maxIter, juliaCx, juliaCy } = e.data
  const imgData = new Uint8ClampedArray(width * height * 4)

  for (let py = 0; py < height; py++) {
    for (let px = 0; px < width; px++) {
      const x0 = cx + (px / width - 0.5) * range * (width / height)
      const y0 = cy + (py / height - 0.5) * range
      let x, y, iter

      if (mode === 'mandelbrot') {
        x = 0; y = 0
        for (iter = 0; iter < maxIter; iter++) {
          const xt = x * x - y * y + x0
          y = 2 * x * y + y0
          x = xt
          if (x * x + y * y > 4) break
        }
      } else {
        x = x0; y = y0
        for (iter = 0; iter < maxIter; iter++) {
          const xt = x * x - y * y + juliaCx
          y = 2 * x * y + juliaCy
          x = xt
          if (x * x + y * y > 4) break
        }
      }

      const idx = (py * width + px) * 4
      if (iter === maxIter) {
        imgData[idx] = 15; imgData[idx + 1] = 10; imgData[idx + 2] = 30; imgData[idx + 3] = 255
      } else {
        const t = iter / maxIter
        imgData[idx] = Math.min(255, Math.floor(9 * (1 - t) * t * t * t * 255) + 20)
        imgData[idx + 1] = Math.min(255, Math.floor(15 * (1 - t) * (1 - t) * t * t * 255) + 10)
        imgData[idx + 2] = Math.min(255, Math.floor(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255) + 40)
        imgData[idx + 3] = 255
      }
    }
  }

  self.postMessage({ imgData, width, height }, [imgData.buffer])
}
