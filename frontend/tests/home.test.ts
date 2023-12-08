import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);
}, { timeout: 10000 });

test('can go to report', async ({ page }) => {
	await page.click('text=Translation Report');
	await page.waitForNavigation();

	await expect(page.locator('text=Translation Report')).toBeVisible();
}, { timeout: 10000 });

test('can go to project', async ({ page }) => {
	await page.click('text=GPT MT Benchmarks');
	await page.waitForNavigation();

	await expect(page.locator('text=GPT MT Benchmarks')).toBeVisible();
}, { timeout: 10000 });
