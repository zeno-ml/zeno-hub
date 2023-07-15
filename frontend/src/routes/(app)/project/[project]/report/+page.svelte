<script lang="ts">
	import ReportHomeBlock from '$lib/components/report/ReportHomeBlock.svelte';
	import { chartDefaults } from '$lib/components/report/reportUtil';
	import { projectConfig } from '$lib/stores';
	import { charts } from '$lib/stores.js';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Svg } from '@smui/common';
	import { Icon } from '@smui/icon-button';
</script>

<div class="reports-container">
	<div class="header">
		<h3>Reports</h3>
	</div>
	<div class="reports">
		{#each $charts as chart}
			<ReportHomeBlock {chart} />
		{/each}
		<div
			class="add-reports"
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
	.reports-container {
		display: flex;
		flex-direction: column;
		margin: 20px;
		width: 100%;
	}
	.reports {
		display: flex;
		flex-wrap: wrap;
		overflow-y: auto;
	}
	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.add-reports {
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
	.add-reports:hover {
		background: #f0ebf4;
	}
	.add-button {
		width: 24px;
		height: 24px;
		margin: 14px;
	}
</style>
