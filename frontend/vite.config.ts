import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import { backendEndpoint } from './src/lib/config';

export default defineConfig({
	server: {
		proxy: {
			'/localzeno': {
				target: backendEndpoint,
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
