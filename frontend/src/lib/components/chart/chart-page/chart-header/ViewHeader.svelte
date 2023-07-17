<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import type { Chart } from '$lib/zenoapi';
	import { mdiArrowCollapseLeft } from '@mdi/js';
	import Button, { Label } from '@smui/button';
	import { Svg } from '@smui/common';
	export let isChartEdit: boolean;

	export let chart: Chart;

	let ishover = false;
	let blur = function (ev) {
		ev.target.blur();
	};
</script>

<div class="header">
	<div
		class="return-link"
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
		<Svg style="width: 24px; height: 24px; padding-right: 10px" viewBox="-2 -2 26 26">
			<path fill={ishover ? 'black' : 'var(--G2)'} d={mdiArrowCollapseLeft} />
		</Svg>
		<h4 style={ishover ? 'color:black' : 'color:var(--G2)'}>Back to Chart Home</h4>
	</div>
	<div class="title-flex">
		<h2 style="margin:0px 20px 0px 0px; color: var(--G2)">
			{chart.name}
		</h2>
		<Button
			style="width: 24px; height: 24px;background-color:var(--G5)"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => (isChartEdit = !isChartEdit)}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
	</div>
</div>

<style>
	.header {
		width: calc(50vw);
		display: flex;
		flex-direction: column;
		width: 353px;
		min-width: 353px;
		max-width: 353px;
		padding-top: 10px;
		padding-bottom: 0px;
		padding-left: 15px;
		padding-right: 15px;
	}

	.return-link {
		display: flex;
		align-items: center;
		cursor: pointer;
		width: fit-content;
		margin-bottom: 5px;
	}
	.title-flex {
		display: flex;
		align-items: center;
	}
</style>
