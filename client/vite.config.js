import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        // 기본 메인 페이지 (기존 index.html)
        main: resolve(__dirname, 'index.html'),
        
        // 추가할 어드민 페이지
        admin: resolve(__dirname, 'admin/admin.html'),

        result : resolve(__dirname, 'result/result.html')
      },
    },
  },
})