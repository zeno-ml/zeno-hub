import { test } from '@playwright/test';

test('can go to home', async ({ page }) => {
	await page.goto('/');
});

test('can login', async ({ page }) => {
	await page.goto('/login');
	await page.fill('input[name="username"]', 'test');
	await page.fill('input[name="password"]', 'Test1212!');
	await page.click('button[type="submit"]');
});
