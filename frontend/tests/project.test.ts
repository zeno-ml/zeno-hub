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
	await expect(page.getByRole('button', { name: 'short arabic 38.20 (1,525)' })).toBeVisible();
});

test('can filter by slice', async ({ page }) => {
	await page.getByText('short arabic').click();
	const grid = await page.locator('.grid').first();
	await expect(grid.getByRole('button').first()).toHaveText(
		' People may not anticipate that patience and understanding are also necessary for travellers returning home. label: ممكن ما يتوقع الناس أن الصبر والتفاهم ضروريات أيضاً للمسافرين الراجعين لبلدانهم.  output: الناس ممكن ما يتوقعوا إن الصبر والتفهم لازمين كمان للمسافرين اللي راجعين البيت.'
	);
});

test('can filter by tag', async ({ page }) => {
	await page.getByText('random tag').click();
	const grid = await page.locator('.grid').first();
	await expect(grid.getByRole('button').first()).toHaveText(
		'"We now have 4-month-old mice that are non-diabetic that used to be diabetic," he added. label: Mums tagad ir 4 mēnešus vecas peles, kas nav diabēta slimnieces, bet kuras agrāk bija diabēta slimnieces, viņš piebilda.  output: "Mums tagad ir četru mēnešu veci peliņi, kas nav diabētiski, bet agrāk bija diabētiski," viņš piebilda.'
	);
});
