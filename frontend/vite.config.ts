import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(root, './src'),
      '@app': path.resolve(root, './src/app'),
      '@components': path.resolve(root, './src/components'),
      '@features': path.resolve(root, './src/features'),
      '@hooks': path.resolve(root, './src/hooks'),
      '@contexts': path.resolve(root, './src/contexts'),
      '@store': path.resolve(root, './src/store'),
      '@services': path.resolve(root, './src/services'),
      '@utils': path.resolve(root, './src/utils'),
      '@app-types': path.resolve(root, './src/types'),
      '@constants': path.resolve(root, './src/constants'),
      '@styles': path.resolve(root, './src/styles'),
      '@assets': path.resolve(root, './src/assets'),
      '@design-system': path.resolve(root, './src/design-system'),
    },
  },
  build: {
    target: 'esnext',
    minify: 'terser',
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-three': ['three'],
        },
      },
    },
  },
});
