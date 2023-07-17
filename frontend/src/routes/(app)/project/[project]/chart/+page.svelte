<script lang="ts">
	import ChartHomeBlock from '$lib/components/chart/ChartHomeBlock.svelte';
	import { chartDefaults } from '$lib/components/chart/chartUtil';
	import { projectConfig } from '$lib/stores';
	import { charts } from '$lib/stores.js';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Svg } from '@smui/common';
	import { Icon } from '@smui/icon-button';
</script>

<div class="charts-container">
	<div class="header">
		<h3>Charts</h3>
	</div>
	<div class="charts">
		{#each $charts as chart}
			<ChartHomeBlock {chart} />
		{/each}
		<div
			class="add-charts"
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
			on:keydown={() => ({})}
		>
			<div class="add-button">
				<Icon style="outline:none" component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiPlus} />
				</Icon>
			</div>
		</div>
	</div>
</div>

<style>
	.charts-container {
		display: flex;
		flex-direction: column;
		margin: 20px;
		width: 100%;
	}
	.charts {
		display: flex;
		flex-wrap: wrap;
		overflow-y: auto;
	}
	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.add-charts {
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		align-items: center;
		border: 1px solid var(--G4);
		border-radius: 10px;
		margin: 5px 5px 5px 5px;
		padding-left: 10px;
		padding-right: 10px;
		overflow: visible;
		cursor: pointer;
		width: 225px;
		height: 100px;
	}
	.add-charts:hover {
		background: #f0ebf4;
	}
	.add-button {
		width: 24px;
		height: 24px;
		margin: 14px;
	}
</style>
