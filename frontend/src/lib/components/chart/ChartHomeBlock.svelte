<script lang="ts">
	import {
		mdiBee,
		mdiChartBar,
		mdiChartLine,
		mdiDotsHorizontal,
		mdiRadar,
		mdiTable,
		mdiViewGrid
	} from '@mdi/js';

	import { goto, invalidate } from '$app/navigation';
	import { page } from '$app/stores';
	import { charts, project } from '$lib/stores';
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
	class="flex flex-col items-center mr-2 mb-2 border border-grey-lighter rounded-lg hover:bg-primary-ligther cursor-pointer max-w-[500px]"
	on:click={() => goto(`${$page.url}/${chart.id}?edit=false`)}
>
	<div class="flex justify-between items-center w-full">
		<div class="m-4 min-w-[24px]">
			<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={iconMap[chart.type]} />
			</Icon>
		</div>
		<h3 class="text-lg">{chart.name}</h3>
		<div>
			<IconButton
				class="ml-2"
				on:click={(e) => {
					e.stopPropagation();
					showOptions = !showOptions;
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiDotsHorizontal} />
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
									ZenoService.addChart($project ? $project.uuid : '', {
										id: 0,
										name: 'Copy of ' + chart.name,
										type: chart.type,
										parameters: chart.parameters
									}).then((res) => {
										invalidate('app:chart');
										charts.update((c) => {
											c.push({
												id: res,
												name: 'Copy of ' + chart.name,
												type: chart.type,
												parameters: chart.parameters
											});
											return c;
										});
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
										charts.update((c) => c.filter((c) => c.id !== chart.id));
										invalidate('app:chart');
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
