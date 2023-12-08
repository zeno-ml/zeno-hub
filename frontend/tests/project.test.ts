import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);
	await page.click('text=GPT MT Benchmarks');
	await page.waitForNavigation();
}, { timeout: 10000 });

test('can see project header', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});

test('slice and tags are present', async ({ page }) => {
	await expect(page.locator('text=All instances')).toBeVisible();
	await expect(page.locator('text=short latin')).toBeVisible();
	await expect(page.locator('text=random tag')).toBeVisible();
}, { timeout: 10000 });

test('can filter by slice', async ({ page }) => {
	await page.click('text=short latin');
	const grid = await page.locator('.grid').first();
	await expect(grid.locator('text=That didn\'t seem to make sense to me; it certainly wasn\'t fair.')).toBeVisible();
}, { timeout: 10000 });

test('can filter by tag', async ({ page }) => {
	await page.click('text=random tag');
	const grid = await page.locator('.grid').first();
	await expect(grid.locator('text=All I say to people is you treat us the way we treat you.')).toBeVisible();
}, { timeout: 10000 });
