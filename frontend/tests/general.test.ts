import { test } from '@playwright/test';
import { login } from './login';

test('can go to home', async ({ page }) => {
	await page.goto('/');
});

test('can login', async ({ page }) => {
	await login(page);
});
