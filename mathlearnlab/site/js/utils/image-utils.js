// Client-side image compression using Canvas API

const ImageUtils = {
  /**
   * Compress image and return base64-encoded JPEG.
   * @param {File|Blob} file - Image file
   * @param {number} maxSize - Max dimension (width or height)
   * @param {number} quality - JPEG quality 0-1
   * @returns {Promise<{base64: string, bytes: number}>}
   */
  async compress(file, maxSize = 1200, quality = 0.8) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          // Calculate new dimensions
          let { width, height } = img;
          if (width > maxSize || height > maxSize) {
            const scale = maxSize / Math.max(width, height);
            width = Math.round(width * scale);
            height = Math.round(height * scale);
          }

          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          const base64 = canvas.toDataURL('image/jpeg', quality);
          // Strip the data:image/jpeg;base64, prefix
          const pureBase64 = base64.split(',')[1];
          const bytes = Math.round(pureBase64.length * 3 / 4);

          resolve({ base64: pureBase64, bytes });
        };
        img.onerror = reject;
        img.src = e.target.result;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  },

  /**
   * Read file as data URL for preview.
   */
  readAsDataUrl(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  },

  /**
   * Validate that a file is an image.
   */
  isImage(file) {
    return file && file.type.startsWith('image/');
  },
};
