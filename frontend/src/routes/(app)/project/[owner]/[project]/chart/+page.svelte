<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import ChartHomeBlock from '$lib/components/chart/ChartHomeBlock.svelte';
	import { chartDefaults } from '$lib/components/chart/chartUtil';
	import { project } from '$lib/stores';
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
		<h3 class="text-xl mb-3">Charts</h3>
	</div>
	<div class="flex flex-wrap overflow-y-auto">
		{#each $charts as chart}
			<ChartHomeBlock {chart} />
		{/each}
		{#if $project && $project.editor}
			<button
				class="flex flex-col justify-around items-center border border-grey-lighter rounded-lg w-48 hover:bg-primary-light mb-2"
				on:click={() => {
					ZenoService.addChart(
						$project ? $project.uuid : '',
						chartDefaults('New Chart', 0, ChartType.BAR)
					).then((res) => {
						invalidateAll();
						charts.update((c) => [...c, chartDefaults('New Chart', res, ChartType.BAR)]);

						goto(
							`/project/${$project ? $project.ownerName : ''}/${
								$project ? $project.name : ''
							}/chart/${$charts[$charts.length - 1].id}?edit=true`
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
		{/if}
	</div>
</div>
