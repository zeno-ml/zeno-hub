<script lang="ts">
	import { goto } from '$app/navigation';
	import ChartCard from '$lib/components/chart/ChartCard.svelte';
	import ChartConfigPopup from '$lib/components/popups/ChartConfigPopup.svelte';
	import { charts, project } from '$lib/stores';
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import Button from '@smui/button';
	import { Icon } from '@smui/icon-button';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let chartConfigEdit = false;

	$: charts.set(data.charts);
</script>

{#if chartConfigEdit && $project.editor}
	<ChartConfigPopup bind:config={data.chartConfig} on:close={() => (chartConfigEdit = false)} />
{/if}
<div class="flex w-full flex-col p-8 pt-5">
	<div class="mb-1 flex h-12 items-center">
		<h3 class="mr-4 text-2xl">Charts</h3>
		{#if $project.editor}
			<Button
				on:click={() => {
					zenoClient
						.addChart($project.uuid, chartDefaults('New Chart', 0, $project.uuid, ChartType.BAR))
						.then((res) => {
							goto(
								`/project/${$project.uuid}/${encodeURIComponent(
									$project.name
								)}/chart/${res}?edit=true`
							);
						});
				}}
			>
				<Icon class="mr-2" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
					<path d={mdiPlus} />
				</Icon>
				New Chart
			</Button>
			<Button
				class="ml-auto mt-2 shrink-0 sm:mt-0"
				variant="outlined"
				on:click={() => (chartConfigEdit = true)}>Chart Configuration</Button
			>
		{/if}
	</div>
	<div class="mb-6 h-0.5 w-full rounded-full bg-grey-light" />
	<div class="mb-4 grid h-full grid-cols-home content-start gap-5 overflow-y-auto">
		{#each $charts.sort((a, b) => a.id - b.id) as chart}
			<ChartCard {chart} />
		{/each}
	</div>
</div>
