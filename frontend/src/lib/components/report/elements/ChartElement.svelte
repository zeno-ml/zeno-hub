<script lang="ts">
	import Spinner from '$lib/components/general/Spinner.svelte';
	import { chartMap } from '$lib/util/charts';
	import { ChartType, type Chart, type ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	const zenoClient = getContext('zenoClient') as ZenoService;

	export let chart: Chart;
	export let width: number;

	$: chartData = zenoClient.getChartData(chart.projectUuid, chart.id);
</script>

{#await chartData}
	<div class="m-auto w-full text-center">
		<Spinner />
	</div>
{:then data}
	<div class="w-full">
		<h3 class="text-lg font-semibold">{chart.name}</h3>
		<div>
			<svelte:component
				this={chartMap[chart.type]}
				{chart}
				{width}
				data={JSON.parse(data)}
				height={chart.type == ChartType.RADAR ? 600 : 400}
			/>
		</div>
	</div>
{/await}
