import { expect, test } from '@playwright/test';

test('can go to home', async ({ page }) => {
	await page.goto('/');
});

test('can login', async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();

	// Should have profile button with first two letters, in this case 'te' for 'test'
	await expect(page.getByRole('button', { name: 'te', exact: true })).toBeVisible();
});
