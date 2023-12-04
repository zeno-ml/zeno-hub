import { expect, test } from '@playwright/test';
import { login } from './login';

test.beforeEach(async ({ page }) => {
	await login(page);

	await page.getByRole('button', { name: 'Translation Report' }).click();
	await page.waitForURL('/report/**');
});

test('can see report elements', async ({ page }) => {
	await expect(page.getByRole('heading', { name: 'Translation Report' })).toBeVisible();
	await expect(page.getByText('Here is my new report.')).toBeVisible();
	await expect(page.getByText('Slice short latin model GPT4 five-shot')).toBeVisible();
	await expect(
		page.getByText('Water is spilling over the levee in a section 100 feet wide.')
	).toBeVisible();
	await expect(
		page.getByText("It's worth half an hour to stroll about the intriguing village.")
	).toBeVisible();
	await expect(page.getByText('Tag random tag model ChatGPT five-shot')).toBeVisible();
	await expect(
		page.getByText(
			'The United States Strategic Command of the U.S. Department of Defense office is tracking the debris.'
		)
	).toBeVisible();
	await expect(
		page.getByText(
			"Accepted were Aristotle's views on all matters of science, including psychology"
		)
	).toBeVisible();
	await expect(page.getByText('Bar Chart')).toBeVisible();
	await expect(page.locator('.mark-rect')).toBeVisible();
});
