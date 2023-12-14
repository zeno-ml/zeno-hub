import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);
});

test('can go to report', async ({ page }) => {
	await page.getByRole('button', { name: 'Translation Report' }).click();
	await expect(page.getByRole('heading', { name: 'Translation Report' })).toBeVisible();
});

test('can go to project', async ({ page }) => {
	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();
	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});
