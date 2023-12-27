import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);
});

test('can go to report', async ({ page }) => {
	await page.getByRole('button', { name: 'Translation Report' }).click();

	await page.waitForURL('/report/**');

	await expect(page.getByRole('heading', { name: 'Translation Report', level: 4 })).toBeVisible();
});

test('can go to project', async ({ page }) => {
	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();

	await page.waitForURL('/project/**');

	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});

test('can create report', async ({ page }) => {
	await page.getByRole('button', { name: 'new report' }).click();
	await page.getByRole('textbox', { name: 'report name' }).fill('test report');
	await page.keyboard.down('Enter');
	await expect(page.getByRole('heading', { name: 'test report' })).toBeVisible();
});
