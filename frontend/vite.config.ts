import { connexEndpoint, localzeno } from './src/lib/config';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	server: {
		proxy: {
			'/connex': {
				target: connexEndpoint,
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path.replace(/^\/connex/, '')
			},
			'/localzeno': {
				target: localzeno,
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
