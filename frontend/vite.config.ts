import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react({ jsxRuntime: 'classic' })],
  build: {
    outDir: '../src/refast_grid/static',
    emptyOutDir: true,
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      name: 'RefastRefastGrid',
      fileName: () => 'refast_grid.js',  // Force .js extension
      formats: ['umd'],
    },
    rollupOptions: {
      // React and ReactDOM are provided globally by refast-client.js
      external: ['react', 'react-dom'],
      output: {
        globals: {
          // refast-client.js exposes window.React and window.ReactDOM
          react: 'React',
          'react-dom': 'ReactDOM',
        },
        // Ensure proper UMD output
        name: 'RefastRefastGrid',
        // Ensure CSS is extracted (if you add styles)
        assetFileNames: 'refast_grid[extname]',
        // Force .js extension (not .cjs)
        entryFileNames: 'refast_grid.js',
      },
    },
  },
  define: {
    'process.env': {},
  },
});
