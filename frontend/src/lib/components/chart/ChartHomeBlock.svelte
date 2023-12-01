<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { project } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import {
		mdiBee,
		mdiChartBar,
		mdiChartLine,
		mdiDotsHorizontal,
		mdiRadar,
		mdiTable,
		mdiViewGrid
	} from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';
	import Confirm from '../popups/Confirm.svelte';

	export let chart: Chart;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showOptions = false;
	let showDelete = false;
	let iconMap = {
		[ChartType.TABLE]: mdiTable,
		[ChartType.LINE]: mdiChartLine,
		[ChartType.BAR]: mdiChartBar,
		[ChartType.BEESWARM]: mdiBee,
		[ChartType.RADAR]: mdiRadar,
		[ChartType.HEATMAP]: mdiViewGrid
	};
</script>

{#if showDelete}
	<Confirm
		message={'Are you sure you want to delete this chart?'}
		on:confirm={() => {
			showOptions = false;
			zenoClient.deleteChart($project.uuid, chart.id).then(() => invalidate('app:charts'));
		}}
		on:cancel={() => (showDelete = false)}
	/>
{/if}
<button
	class="mb-4 mr-4 flex flex-col rounded-sm border border-solid border-grey-light px-5 py-1 shadow-sm hover:shadow-md"
	on:click={() => goto(`chart/${chart.id}?edit=false`)}
>
	<div class="flex w-full items-center justify-between">
		<div class="mr-3 min-w-[24px]">
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
				<button
					class="absolute z-10 ml-5"
					use:clickOutside={() => (showOptions = !showOptions)}
					on:click={(e) => e.stopPropagation()}
					on:keydown={(e) => {
						if (e.key === 'Escape') {
							showOptions = false;
						}
					}}
				>
					<Paper style="padding: 7px 0px 7px 0px;" elevation={7}>
						<Content>
							<button
								class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									zenoClient
										.addChart($project.uuid, {
											id: 0,
											name: 'Copy of ' + chart.name,
											type: chart.type,
											projectUuid: $project.uuid,
											parameters: chart.parameters
										})
										.then(() => invalidate('app:charts'));
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">content_copy</Icon>&nbsp;
								<span class="text-sm">Make a copy</span>
							</button>
							<button
								class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									showDelete = true;
								}}
							>
								<Icon style="font-size: 20px;" class="material-icons">delete_outline</Icon>&nbsp;
								<span class="text-sm">Delete</span>
							</button>
						</Content>
					</Paper>
				</button>
			{/if}
		</div>
	</div>
</button>
