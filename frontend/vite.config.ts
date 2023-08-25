import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	server: {
		proxy: {
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
