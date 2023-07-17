<script lang="ts">
	import { page } from '$app/stores';
	import type { Chart } from '$lib/zenoapi';
	import { mdiArrowCollapseLeft } from '@mdi/js';
	import Button, { Label } from '@smui/button';
	import { Svg } from '@smui/common';
	import Textfield from '@smui/textfield';
	import { noop } from 'svelte/internal';

	export let isChartEdit: boolean;
	export let chart: Chart;
	export let updateChart: () => void = noop;

	let ishover = false;
	let blur = function (ev) {
		ev.target.blur();
	};
</script>

<div class="header-flex">
	<div class="top-flex">
		<a
			class="return-link"
			href={$page.url.href.substring(0, $page.url.href.lastIndexOf('/'))}
			on:click={updateChart}
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
		</a>
		<Button
			style="width: 24px; height: 24px;margin-bottom:3px;background-color:var(--G5)"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => {
				isChartEdit = !isChartEdit;
				updateChart();
			}}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
	</div>
	<div>
		<Textfield
			style="width: -webkit-fill-available"
			variant="outlined"
			bind:value={chart.name}
			label="Chart Name"
		/>
	</div>
</div>

<style>
	.header-flex {
		display: flex;
		flex-direction: column;
	}
	.top-flex {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.return-link {
		display: flex;
		align-items: center;
		cursor: pointer;
		width: fit-content;
		margin-bottom: 5px;
	}
</style>
