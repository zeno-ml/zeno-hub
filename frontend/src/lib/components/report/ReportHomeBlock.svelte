<script lang="ts">
	import {
		mdiBee,
		mdiChartBar,
		mdiChartLine,
		mdiDotsVertical,
		mdiRadar,
		mdiTable,
		mdiViewGrid
	} from '@mdi/js';

	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { currentProject, charts } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import { Svg } from '@smui/common';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';

	export let chart: Chart;

	let showOptions = false;
	let iconMap = {
		[ChartType.TABLE]: mdiTable,
		[ChartType.LINE]: mdiChartLine,
		[ChartType.BAR]: mdiChartBar,
		[ChartType.BEESWARM]: mdiBee,
		[ChartType.RADAR]: mdiRadar,
		[ChartType.HEATMAP]: mdiViewGrid
	};
</script>

<div class="report" on:click={() => goto(`${$page.url}/${chart.id}`)} on:keydown={() => ({})}>
	<div class="inline">
		<div class="report-type">
			<Icon style="outline:none" component={Svg} viewBox="0 0 24 24">
				<path fill="black" d={iconMap[chart.type]} />
			</Icon>
		</div>
		<p class="report-name">{chart.name}</p>
		<div>
			<IconButton
				on:click={(e) => {
					e.stopPropagation();
					showOptions = !showOptions;
				}}
			>
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiDotsVertical} />
				</Icon>
			</IconButton>
			{#if showOptions}
				<div
					id="options-container"
					use:clickOutside
					on:clickOutside={() => (showOptions = !showOptions)}
				>
					<Paper style="padding: 7px 0px 7px 0px;" elevation={7}>
						<Content>
							<div
								class="option"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									ZenoService.addChart($currentProject ? $currentProject.uuid : '', {
										id: 0,
										name: 'Copy of ' + chart.name,
										type: chart.type,
										parameters: chart.parameters
									}).then(() => {
										ZenoService.getCharts($currentProject ? $currentProject.uuid : '').then(
											(fetchedCharts) => charts.set(fetchedCharts)
										);
									});
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">content_copy</Icon>&nbsp;
								<span>Make a copy</span>
							</div>
							<div
								class="option"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									ZenoService.deleteChart(chart).then(() => {
										ZenoService.getCharts($currentProject ? $currentProject.uuid : '').then(
											(fetchedCharts) => charts.set(fetchedCharts)
										);
									});
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">delete_outline</Icon>&nbsp;
								<span>Remove</span>
							</div>
						</Content>
					</Paper>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.report {
		display: flex;
		flex-direction: column;
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
	.report:hover {
		background: var(--P3);
	}
	.inline {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		width: 100%;
	}
	.report-type {
		width: 24px;
		height: 24px;
		margin: 14px;
	}
	.report-name {
		font-size: 16px;
		color: black;
		text-overflow: ellipsis;
		overflow: hidden;
		max-width: 100%;
		white-space: nowrap;
	}
	#options-container {
		z-index: 5;
		margin-top: -7px;
		margin-left: 20px;
		position: absolute;
	}
	.option {
		display: flex;
		flex-direction: row;
		align-items: center;
		cursor: pointer;
		width: 110px;
		padding: 2px 10px 2px 10px;
	}
	.option span {
		font-size: 13px;
	}
	.option:hover {
		background: var(--G5);
	}
</style>
