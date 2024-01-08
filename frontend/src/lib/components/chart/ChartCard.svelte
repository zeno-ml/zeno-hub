<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { project } from '$lib/stores';
	import { chartMap } from '$lib/util/charts';
	import { clickOutside } from '$lib/util/clickOutside';
	import { tooltip } from '$lib/util/tooltip';
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
	import { getContext } from 'svelte';
	import Spinner from '../general/Spinner.svelte';
	import Confirm from '../popups/Confirm.svelte';
	import ChartOptions from './ChartOptions.svelte';

	export let chart: Chart;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showOptions = false;
	let hovering = false;
	let showDelete = false;
	let iconMap = {
		[ChartType.TABLE]: mdiTable,
		[ChartType.LINE]: mdiChartLine,
		[ChartType.BAR]: mdiChartBar,
		[ChartType.BEESWARM]: mdiBee,
		[ChartType.RADAR]: mdiRadar,
		[ChartType.HEATMAP]: mdiViewGrid
	};
	let width;
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
	on:click={() => goto(`chart/${chart.id}?edit=false`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => {
		hovering = false;
		showOptions = false;
	}}
	on:blur={() => {
		hovering = false;
		showOptions = false;
	}}
	class="flex h-full w-full flex-col rounded-md border border-solid border-grey-light bg-white hover:shadow-sm"
>
	<div class="mt-2 flex h-9 w-full items-center px-3">
		<Icon tag="svg" viewBox="0 0 24 24">
			<path fill="black" d={iconMap[chart.type]} />
		</Icon>
		<div class="flex pl-2" use:tooltip={{ text: chart.name }}>
			<p class="line-clamp-1 text-xl text-black">
				{chart.name}
			</p>
		</div>
		<div
			class="relative ml-auto mt-1"
			use:clickOutside={() => {
				showOptions = false;
			}}
		>
			<button
				class="rounded-md {project ? 'hover:bg-project-light' : 'hover:bg-report-light'} {hovering
					? 'visible'
					: 'invisible'}"
				on:click={(e) => {
					e.stopPropagation();
					showOptions = !showOptions;
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiDotsHorizontal} />
				</Icon>
			</button>
			{#if showOptions}
				<ChartOptions bind:showOptions bind:showDelete {chart} />
			{/if}
		</div>
	</div>
	{#await zenoClient.getChartConfig(chart.projectUuid, chart.id) then chartConfig}
		{#await zenoClient.getChartData($project.uuid, chart.id)}
			<Spinner width={24} height={24} />
		{:then chartData}
			{#if chartData}
				<div
					class="flex aspect-square w-full justify-center overflow-hidden text-center {chart.type !==
					ChartType.TABLE
						? 'items-center'
						: ''}"
					bind:clientWidth={width}
				>
					<svelte:component
						this={chartMap[chart.type]}
						{chart}
						{chartConfig}
						preview={true}
						data={JSON.parse(chartData)}
						width={width - 70}
						height={width - 70}
					/>
				</div>
			{/if}
		{/await}
	{:catch error}
		<p class="ml-4 mt-4 font-semibold text-error">
			Chart config could not be loaded: {error.message}
		</p>
	{/await}
</button>
