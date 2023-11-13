import { getClientAndUser } from '$lib/api/client';
import type { ApiError, ReportResponse } from '$lib/zenoapi';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url }) {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	let reportResponse: ReportResponse;
	try {
		reportResponse = await zenoClient.getReport(parseInt(params.id));
	} catch (e: unknown) {
		if ((e as ApiError).status === 401) {
			if (cognitoUser !== null) {
				throw redirect(303, `/auth`);
			} else {
				throw redirect(303, `/login?redirectTo=${url.pathname}`);
			}
		} else {
			// try to route using owner/report_name for legacy reports.
			try {
				reportResponse = await zenoClient.getReportByName(
					params.id,
					encodeURIComponent(params.name)
				);
			} catch (e: unknown) {
				throw error(404, 'Could not load report');
			}
			throw redirect(
				301,
				`/report/${reportResponse.report.id}/${encodeURIComponent(reportResponse.report.name)}`
			);
		}
	}

	if (reportResponse.report.name !== decodeURI(params.name)) {
		throw redirect(
			301,
			`/report/${reportResponse.report.id}/${encodeURIComponent(reportResponse.report.name)}`
		);
	}

	return {
		report: reportResponse.report,
		reportElements: reportResponse.reportElements,
		cognitoUser: cognitoUser,
		numLikes: reportResponse.numLikes,
		userLiked: reportResponse.userLiked
	};
}
