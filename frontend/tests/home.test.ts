import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();
	await page.waitForURL('/home/test');
	await page.waitForSelector('body.started', { timeout: 5000 });
});

test('can go to report', async ({ page }) => {
	await page.getByRole('button', { name: 'Translation Report' }).click();

	await page.waitForURL('/report/**');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await expect(page.getByRole('heading', { name: 'Translation Report' })).toBeVisible();
});

test('can go to project', async ({ page }) => {
	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();

	await page.waitForURL('/project/**');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});
