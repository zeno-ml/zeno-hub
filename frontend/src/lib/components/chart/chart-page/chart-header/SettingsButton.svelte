<script lang="ts">
	import CircleIconButton from '$lib/components/general/CircleIconButton.svelte';
	import ChartConfigPopup from '$lib/components/popups/ChartConfigPopup.svelte';
	import { project } from '$lib/stores';
	import type { Chart, ChartConfig } from '$lib/zenoapi';
	import { mdiCog } from '@mdi/js';

	export let chart: Chart;
	export let chartConfig: ChartConfig;

	let chartConfigEdit = false;
</script>

{#if chartConfigEdit && $project.editor}
	<ChartConfigPopup
		bind:config={chartConfig}
		chartId={chart.id}
		on:close={() => (chartConfigEdit = false)}
	/>
{/if}

<CircleIconButton icon={mdiCog} on:click={() => (chartConfigEdit = true)} positioning="ml-auto" />
