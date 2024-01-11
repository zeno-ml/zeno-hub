import type { Page } from '@playwright/test';

export async function login(page: Page) {
	await page.goto('/login');

	await page.getByLabel('Username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('Password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();
}
