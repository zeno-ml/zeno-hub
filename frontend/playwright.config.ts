import type { PlaywrightTestConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config({ path: './.env' });

const config: PlaywrightTestConfig = {
	reporter: 'html',
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	retries: 2,
	use: {
		baseURL: 'http://localhost:5173'
	}
};

export default config;
