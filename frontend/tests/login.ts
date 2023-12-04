import type { Page } from '@playwright/test';

export async function login(page: Page) {
	await page.goto('/login');
	await page.waitForTimeout(1000);

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();

	await page.waitForURL('/home/test');
	await page.waitForTimeout(1000);
}
