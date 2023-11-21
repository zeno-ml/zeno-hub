import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();
});

test('can create report', async ({ page }) => {
	await page.goto('/home/test');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await page.getByRole('button', { name: 'New Report' }).click();
	await page.getByPlaceholder(' ').fill('Test Report');
	await page.getByRole('button', { name: 'Create', exact: true }).click();

	await page.waitForURL('/report/**');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await expect(page.getByRole('heading', { name: 'Test Report' })).toBeVisible();
});

test('can delete report', async ({ page }) => {
	await page.goto('/home/test');

	await page.getByRole('button', { name: 'Test Report' }).hover();
	await page.getByRole('button', { name: 'Test Report' }).getByRole('button').first().click();
	await page.getByRole('button', { name: 'Remove', exact: true }).click();
	await page.getByRole('button', { name: 'Confirm' }).click();
	await expect(page.getByRole('button', { name: 'Test Report' })).not.toBeVisible();
});
