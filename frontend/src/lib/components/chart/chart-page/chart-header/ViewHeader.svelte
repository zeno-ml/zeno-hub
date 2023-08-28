<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { project } from '$lib/stores';
	import type { Chart } from '$lib/zenoapi';
	import { mdiArrowCollapseLeft } from '@mdi/js';
	import Button, { Label } from '@smui/button';
	import { SmuiElement } from '@smui/common';

	export let isChartEdit: boolean | undefined;
	export let chart: Chart;

	let ishover = false;
	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};
</script>

<div class="flex flex-col p-3">
	<div
		class="flex items-center cursor-pointer mb-4"
		on:keydown={() => ({})}
		on:click={() => {
			goto($page.url.href.substring(0, $page.url.href.lastIndexOf('/')));
		}}
		on:focus={() => ({})}
		on:mouseover={() => {
			ishover = true;
		}}
		on:blur={() => ({})}
		on:mouseout={() => {
			ishover = false;
		}}
	>
		<SmuiElement
			tag="svg"
			style="width: 24px; height: 24px; padding-right: 10px"
			viewBox="-2 -2 26 26"
		>
			<path class="fill-{ishover ? 'black' : 'grey-dark'}" d={mdiArrowCollapseLeft} />
		</SmuiElement>
		<h4 class="text-grey-dark hover:text-black">Back to Chart Home</h4>
	</div>
	<div class="flex items-center">
		<h2 class="mr-5 text-grey-dark text-xl">
			{chart.name}
		</h2>
		{#if $project?.editor}
			<Button
				variant="outlined"
				on:mouseleave={blur}
				on:focusout={blur}
				on:click={() => (isChartEdit = !isChartEdit)}
			>
				<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
			</Button>
		{/if}
	</div>
</div>
