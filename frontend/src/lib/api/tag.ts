import { projectConfig } from '$lib/stores';
import { ZenoService, type GroupMetric, type TagMetricKey } from '$lib/zenoapi';
import { get } from 'svelte/store';

export async function getMetricsForTags(tagMetricKey: TagMetricKey): Promise<GroupMetric | null> {
	if (tagMetricKey.metric === undefined || tagMetricKey.model === undefined) {
		return null;
	}
	const project = get(projectConfig);
	if (!project) {
		return Promise.reject('No project selected.');
	}
	return await ZenoService.getMetricForTag(project.uuid, tagMetricKey);
}
