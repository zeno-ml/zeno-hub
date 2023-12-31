import { getClientAndUser } from '$lib/api/client';
import type { ApiError, ReportResponse } from '$lib/zenoapi';
import { error, redirect, type NumericRange } from '@sveltejs/kit';

export async function load({ cookies, params, url, depends }) {
	depends('app:report');

	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	let reportResponse: ReportResponse;
	try {
		reportResponse = await zenoClient.getReport(parseInt(params.id));
	} catch (e: unknown) {
		if ((e as ApiError).status === 401) {
			if (cognitoUser !== null) {
				redirect(303, `/auth`);
			} else {
				redirect(303, `/login?redirectTo=${url.pathname}`);
			}
		} else {
			// try to route using owner/report_name for legacy reports.
			try {
				reportResponse = await zenoClient.getReportByName(
					params.id,
					encodeURIComponent(params.name)
				);
			} catch (e: unknown) {
				const err = e as ApiError;
				error(err.status as NumericRange<400, 599>, err.body.detail);
			}
			redirect(
				301,
				`/report/${reportResponse.report.id}/${encodeURIComponent(reportResponse.report.name)}`
			);
		}
	}
	const [projects, charts, slices, tags, authors, users, owner] = await Promise.all([
		zenoClient.getProjects(reportResponse.report.linkedProjects),
		zenoClient.getChartsForProjects(reportResponse.report.linkedProjects),
		zenoClient.getSlicesForProjects(reportResponse.report.linkedProjects),
		zenoClient.getTagsForProjects(reportResponse.report.linkedProjects),
		zenoClient.getReportAuthors(reportResponse.report.id),
		zenoClient.getReportUsers(reportResponse.report.id),
		zenoClient.getReportOwner(reportResponse.report.id)
	]);

	if (reportResponse.report.name !== decodeURI(params.name)) {
		redirect(
			301,
			`/report/${reportResponse.report.id}/${encodeURIComponent(reportResponse.report.name)}`
		);
	}

	return {
		report: reportResponse.report,
		reportElements: reportResponse.reportElements,
		charts,
		slices,
		tags,
		cognitoUser: cognitoUser,
		numLikes: reportResponse.numLikes,
		userLiked: reportResponse.userLiked,
		projects: projects,
		authors: authors,
		users: [...users, owner]
	};
}
