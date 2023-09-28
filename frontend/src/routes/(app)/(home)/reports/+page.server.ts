import { ZenoService } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');
	depends('app:reports');

	const publicReports = await ZenoService.getPublicReports();

	return {
		publicReports: publicReports
	};
}
