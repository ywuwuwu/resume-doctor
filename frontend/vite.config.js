import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/', // very important!
  server: {
    proxy: {
      '/upload_resume': 'http://localhost:5050'
    }
  }
})

