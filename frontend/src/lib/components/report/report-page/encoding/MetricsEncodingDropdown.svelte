<script lang="ts">
	import { metrics } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let metric: number;

	const dispatch = createEventDispatcher<{
		selected: number;
	}>();

	let options: { value: number; label: string }[] = [];
	let value = 0;

	$metrics.forEach((m) => {
		options.push({ value: m.id, label: m.name });
	});
	value = metric;
</script>

<div class="parameters">
	<h4 class="select-label">&nbsp;</h4>
	<Svelecte
		style="width: 280px; flex:none;"
		bind:value
		{options}
		on:change={(e) => {
			if (e.detail.value !== metric) {
				dispatch('selected', e.detail.value);
			}
		}}
	/>
</div>

<style>
	.parameters {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		padding: 10px;
	}
	.select-label {
		margin: 5px;
	}
</style>
