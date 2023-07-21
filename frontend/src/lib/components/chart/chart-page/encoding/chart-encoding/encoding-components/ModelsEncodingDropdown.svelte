<script lang="ts">
	import { models } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let stringValue: string;

	const dispatch = createEventDispatcher<{
		selected: string;
	}>();

	let options: { value: string; label: string }[] = [];
	let value = stringValue;

	// initial options & values
	$models.forEach((m) => {
		options.push({ value: m, label: m });
	});

	function valueSelected(e: CustomEvent) {
		if (e.detail.value !== stringValue) {
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
