import type { PlaywrightTestConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

const config: PlaywrightTestConfig = {
	workers: 1,
	reporter: 'html',
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	retries: 1,
	use: {
		baseURL: 'http://localhost:5173'
	}
};

export default config;
