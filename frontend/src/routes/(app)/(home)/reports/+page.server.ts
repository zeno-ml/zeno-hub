import { getEndpoint } from '$lib/api/util';
import { ZenoClient } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');
	depends('app:reports');

	const zenoClient = new ZenoClient({
		BASE: getEndpoint()
	}).zeno;
	const publicReports = await zenoClient.getPublicReportsDetails();

	return {
		publicReports: publicReports
	};
}
