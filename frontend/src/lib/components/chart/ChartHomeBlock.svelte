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
	import { charts, projectConfig } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
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

<button
	class="flex flex-col items-center border-2 border-grey-lighter rounded-lg m-2 hover:bg-primary-light w-48 h-24"
	on:click={() => goto(`${$page.url}/${chart.id}`)}
>
	<div class="flex justify-between items-center w-full">
		<div class="w-5 h-5 m-4">
			<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={iconMap[chart.type]} />
			</Icon>
		</div>
		<p class="color-black">{chart.name}</p>
		<div>
			<IconButton
				on:click={(e) => {
					e.stopPropagation();
					showOptions = !showOptions;
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiDotsVertical} />
				</Icon>
			</IconButton>
			{#if showOptions}
				<div class="z-10 absolute ml-5" use:clickOutside={() => (showOptions = !showOptions)}>
					<Paper style="padding: 7px 0px 7px 0px;" elevation={7}>
						<Content>
							<div
								class="flex items-center cursor-pointer hover:bg-grey-lighter mx-2"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									ZenoService.addChart($projectConfig ? $projectConfig.uuid : '', {
										id: 0,
										name: 'Copy of ' + chart.name,
										type: chart.type,
										parameters: chart.parameters
									}).then(() => {
										ZenoService.getCharts($projectConfig ? $projectConfig.uuid : '').then(
											(fetchedCharts) => charts.set(fetchedCharts)
										);
									});
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">content_copy</Icon>&nbsp;
								<span class="text-sm">Make a copy</span>
							</div>
							<div
								class="flex items-center cursor-pointer hover:bg-grey-lighter mx-2"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									ZenoService.deleteChart(chart).then(() => {
										ZenoService.getCharts($projectConfig ? $projectConfig.uuid : '').then(
											(fetchedCharts) => charts.set(fetchedCharts)
										);
									});
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">delete_outline</Icon>&nbsp;
								<span class="text-sm">Delete</span>
							</div>
						</Content>
					</Paper>
				</div>
			{/if}
		</div>
	</div>
</button>
