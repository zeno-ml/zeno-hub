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
			}
		},
		fs: {
			allow: ['.yalc']
		}
	},
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
