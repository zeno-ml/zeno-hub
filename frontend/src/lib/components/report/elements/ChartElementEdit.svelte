<script lang="ts">
	import { svelecteRendererName } from '$lib/util/util';
	import type { Chart, ReportElement, ZenoService } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let element: ReportElement;
	export let chartOptions: Chart[];
	export let reportId: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let chartId: number = parseInt(element.data as string);

	function updateChartId(e: CustomEvent) {
		element.data = `${e.detail.id}`;
		zenoClient.updateReportElement(reportId, { ...element, data: element.data });
	}
</script>

{#await zenoClient.getProjects() then projects}
	{@const options = chartOptions.map((c) => {
		return {
			name: `${c.name} (${projects.find((p) => p.uuid === c.projectUuid)?.name})`,
			id: c.id
		};
	})}
	<Svelecte
		value={chartId}
		{options}
		valueField="id"
		labelField="name"
		on:change={updateChartId}
		renderer={svelecteRendererName}
	/>
{/await}
