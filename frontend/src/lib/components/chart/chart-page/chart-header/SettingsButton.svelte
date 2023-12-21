<script lang="ts">
	import ChartConfigPopup from '$lib/components/popups/ChartConfigPopup.svelte';
	import { project } from '$lib/stores';
	import type { Chart, ChartConfig } from '$lib/zenoapi';
	import Button from '@smui/button';

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
<Button
	class="ml-auto mr-8 mt-2 shrink-0 sm:mt-0"
	variant="outlined"
	on:click={() => (chartConfigEdit = true)}>Settings</Button
>
