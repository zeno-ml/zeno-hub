import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);

	await page.getByRole('button', { name: 'GPT MT Benchmarks' }).click();
	await page.waitForURL('/project/**');
});

test('can see project header', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'GPT MT Benchmarks' })).toBeVisible();
});

test('can see overview table', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'Overview Table' })).toBeVisible();
});

test.describe('explore', () => {
	test.beforeEach(async ({ page }) => {
		await page.locator("button[aria-label='explore']").click();
	});

	test('slice and tags are present', async ({ page }) => {
		await expect(page.getByRole('button', { name: 'All instances' })).toBeVisible();
		await expect(page.getByRole('button', { name: 'short latin' })).toBeVisible();
		await expect(page.getByRole('button', { name: 'random tag' })).toBeVisible();
	});

	test('can filter by slice', async ({ page }) => {
		await page.getByText('short latin').click();
		const grid = await page.locator('.grid').first();
		await expect(grid.getByRole('button').first()).toContainText(
			"That didn't seem to make sense to me; it certainly wasn't fair."
		);
	});

	test('can filter by tag', async ({ page }) => {
		await page.getByText('random tag').click();
		const grid = await page.locator('.grid').first();
		await expect(grid.getByRole('button').first()).toContainText(
			'All I say to people is you treat us the way we treat you.'
		);
	});
});
