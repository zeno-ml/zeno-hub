<script lang="ts">
	import type { Chart, Project, ReportElement, ZenoService } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let element: ReportElement;
	export let reportProjects: Project[];
	export let chartOptions: Chart[];
	export let reportId: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let chartId: number = parseInt(element.data as string);

	$: options = chartOptions.map((c) => {
		return {
			name: `${c.name} (${reportProjects.find((p) => p.uuid === c.projectUuid)?.name})`,
			id: c.id
		};
	});

	function updateChartId(e: CustomEvent) {
		element.data = `${e.detail.id}`;
		zenoClient.updateReportElement(reportId, { ...element, data: element.data });
	}
</script>

<Svelecte value={chartId} {options} valueField="id" labelField="name" on:change={updateChartId} />
