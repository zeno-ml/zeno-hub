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
	await expect(page.getByText('Slice short arabic model GPT4 five-shot')).toBeVisible();
	await expect(
		page.getByText('Television reports show white smoke coming from the plant.')
	).toBeVisible();
	await expect(
		page.getByText('Fire rescue crews eventually doused the fire by 11:35 pm.')
	).toBeVisible();
	await expect(page.getByText('Tag random tag model ChatGPT five-shot')).toBeVisible();
	await expect(
		page.getByText(
			'"We now have 4-month-old mice that are non-diabetic that used to be diabetic," he added.'
		)
	).toBeVisible();
	await expect(
		page.getByText(
			'Dr. Ehud Ur, professor of medicine at Dalhousie University in Halifax, Nova Scotia and chair of the clinical and scientific division of the Canadian Diabetes Association cautioned that the research is still in its early days.'
		)
	).toBeVisible();
	await expect(page.getByText('Bar Chart')).toBeVisible();
	await expect(page.locator('.mark-rect')).toBeVisible();
});
