import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');
	depends('app:reports');

	OpenAPI.BASE = `${getEndpoint()}/api`;

	const publicReports = await ZenoService.getPublicReports();

	return {
		publicReports: publicReports
	};
}
