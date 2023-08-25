import { project } from '$lib/stores';
import { ZenoService, type GroupMetric, type TagMetricKey } from '$lib/zenoapi';
import { get } from 'svelte/store';

export async function getMetricsForTags(tagMetricKey: TagMetricKey): Promise<GroupMetric | null> {
	const config = get(project);
	if (!config) {
		return Promise.reject('No project selected.');
	}
	return await ZenoService.getMetricForTag(config.uuid, tagMetricKey);
}
