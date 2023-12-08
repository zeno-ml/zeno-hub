import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);
	await page.click('text=Translation Report');
	await page.waitForNavigation();
});

test('can see report elements', async ({ page }) => {
	await expect(page.locator('text=Translation Report')).toBeVisible();
	await expect(page.locator('text=Here is my new report.')).toBeVisible();
	await expect(page.locator('text=Slice short latin model GPT4 five-shot')).toBeVisible();
	await expect(page.locator('text=Water is spilling over the levee in a section 100 feet wide.')).toBeVisible();
	await expect(page.locator('text=It\'s worth half an hour to stroll about the intriguing village.')).toBeVisible();
	await expect(page.locator('text=Tag random tag model ChatGPT five-shot')).toBeVisible();
	await expect(
	await expect(page.locator('text=Accepted were Aristotle\'s views on all matters of science, including psychology')).toBeVisible();
	await expect(page.locator('text=Bar Chart')).toBeVisible();
	await expect(page.locator('.mark-rect')).toBeVisible();
}, { timeout: 10000 });
