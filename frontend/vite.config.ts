import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	server: {
		proxy: {
			'/dockerzeno': {
				target: 'http://zeno-backend:8000',
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path.replace(/^\/dockerzeno/, '')
			},
			'/localzeno': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path.replace(/^\/localzeno/, '')
			}
		}
	},
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
