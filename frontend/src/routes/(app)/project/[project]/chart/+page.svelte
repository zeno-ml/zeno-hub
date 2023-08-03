<script lang="ts">
	import ChartHomeBlock from '$lib/components/chart/ChartHomeBlock.svelte';
	import { chartDefaults } from '$lib/components/chart/chartUtil';
	import { projectConfig } from '$lib/stores';
	import { charts } from '$lib/stores.js';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/icon-button';

	export let data;

	$: {
		charts.set(data.charts);
	}
</script>

<div class="flex flex-col m-5 w-full">
	<div class="flex justify-between align-center">
		<h3>Charts</h3>
	</div>
	<div class="flex flex-wrap overflow-y-auto">
		{#each $charts as chart}
			<ChartHomeBlock {chart} />
		{/each}
		<button
			class="flex flex-col justify-around items-center border-2 border-grey-lighter rounded-lg m-2 px-2.5 w-48 h-24 hover:bg-primary-light"
			on:click={() => {
				ZenoService.addChart(
					$projectConfig ? $projectConfig.uuid : '',
					chartDefaults('New Chart', 0, ChartType.BAR)
				).then(() => {
					ZenoService.getCharts($projectConfig ? $projectConfig.uuid : '').then((fetchedCharts) =>
						charts.set(fetchedCharts)
					);
				});
			}}
		>
			<div class="w-6 h-6">
				<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiPlus} />
				</Icon>
			</div>
		</button>
	</div>
</div>
