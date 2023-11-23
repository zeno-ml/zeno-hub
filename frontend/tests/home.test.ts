import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();
	await page.waitForURL('/home/test');
});

test('can go to report', async ({ page }) => {
	await page.getByRole('button', { name: 'Translation Report' }).click();

	await page.waitForURL('/report/**');

	await expect(page.getByRole('heading', { name: 'Translation Report' })).toBeVisible();
});

test('can go to project', async ({ page }) => {
	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();

	await page.waitForURL('/project/**');

	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});
