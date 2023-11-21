import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
	fullyParallel: true,
	reporter: 'html',
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	use: {
		baseURL: 'http://localhost:5173'
	}
};

export default config;
