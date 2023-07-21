<script lang="ts">
	import { metrics } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let numberValue: number;

	const dispatch = createEventDispatcher<{
		selected: number;
	}>();

	let options: { value: number; label: string }[] = [];
	let value = 0;

	$metrics.forEach((m) => {
		options.push({ value: m.id, label: m.name });
	});
	value = numberValue;

	function valueSelected(e: CustomEvent) {
		if (e.detail.value !== numberValue) {
			dispatch('selected', e.detail);
		}
	}
</script>

<div class="parameters">
	<h4 class="select-label">&nbsp;</h4>
	<Svelecte style="width: 280px; flex:none;" bind:value {options} on:change={valueSelected} />
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
