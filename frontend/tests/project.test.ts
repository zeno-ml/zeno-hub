import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();

	await page.waitForURL('/home/test');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();
	await page.waitForURL('/project/**');
	await page.waitForSelector('body.started', { timeout: 5000 });
});

test('can see project elements', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});

test('slice and tag metrics are correct', async ({ page }) => {
	await expect(page.getByRole('button', { name: 'All instances 42.15 (20,240)' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'short latin 31.77 (7)' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'random tag 26.15 (3)' })).toBeVisible();
});

test('can filter by slice', async ({ page }) => {
	await page.getByText('short latin').click();
	const grid = await page.locator('.grid').first();
	await expect(grid.getByRole('button').first()).toHaveText(
		'He built a WiFi door bell, he said. label: Utsi wakhe ibheli ye-WiFi yasemnyango. output: Wagcina umgodi we-WiFi, wathi.'
	);
});

test('can filter by tag', async ({ page }) => {
	await page.getByText('random tag').click();
	const grid = await page.locator('.grid').first();
	await expect(grid.getByRole('button').first()).toHaveText(
		'He built a WiFi door bell, he said. label: Utsi wakhe ibheli ye-WiFi yasemnyango. output: Wagcina umgodi we-WiFi, wathi.'
	);
});
