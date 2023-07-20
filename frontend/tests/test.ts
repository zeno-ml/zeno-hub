import { test } from '@playwright/test';

test('can go to home', async ({ page }) => {
	await page.goto('/');
});
