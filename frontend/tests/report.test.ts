import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/login');

	await page.getByLabel('username').fill(process.env.HUB_USERNAME || '');
	await page.getByLabel('password').fill(process.env.HUB_PASSWORD || '');
	await page.getByRole('button', { name: 'Login' }).click();
	await page.waitForURL('/home/test');
	await page.waitForSelector('body.started', { timeout: 5000 });

	await page.getByRole('button', { name: 'Translation Report' }).click();
	await page.waitForURL('/report/**');
	await page.waitForSelector('body.started', { timeout: 5000 });
});

test('can see report elements', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'Translation Report' })).toBeVisible();
	await expect(page.getByText('Here is my new report.')).toBeVisible();
	await expect(page.getByText('Slice short latin model GPT4 five-shot')).toBeVisible();
	await expect(page.getByText('Heer maakde ‘n Wi-Fi deurbel, zag ‘r.')).toBeVisible();
	await expect(page.getByText('Ya ce, ya gina ƙararrawar ƙofa ta WiFi.')).toBeVisible();
	await expect(page.getByText('Tag random tag model ChatGPT five-shot')).toBeVisible();
	await expect(page.getByText('Utsi wakhe ibheli ye-WiFi yasemnyango.')).toBeVisible();
	await expect(page.getByText('Thóg sé cloigín dorais WiFi, a dúirt sé.')).toBeVisible();
	await expect(page.getByText('Bar Chart')).toBeVisible();
	await expect(page.locator('.mark-rect')).toBeVisible();
});
