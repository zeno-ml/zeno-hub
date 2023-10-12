import { getClientAndUser } from '$lib/api/util';
import type { ApiError } from '$lib/zenoapi';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url }) {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	try {
		const reportResponse = await zenoClient.getReport(params.owner, params.report);
		return {
			report: reportResponse.report,
			reportElements: reportResponse.reportElements,
			cognitoUser: cognitoUser
		};
	} catch (e: unknown) {
		if ((e as ApiError).status === 401) {
			if (cognitoUser !== null) {
				throw redirect(303, `/auth`);
			} else {
				throw redirect(303, `/login?redirectTo=${url.pathname}`);
			}
		}
		throw error(404, 'Could not load report');
	}
}
