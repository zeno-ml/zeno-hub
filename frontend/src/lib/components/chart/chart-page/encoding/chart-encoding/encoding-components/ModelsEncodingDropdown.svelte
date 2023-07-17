<script lang="ts">
	import { models } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let model: string;

	const dispatch = createEventDispatcher<{
		selected: string;
	}>();

	let options: { value: string; label: string }[] = [];
	let value = model;

	// initial options & values
	$models.forEach((m) => {
		options.push({ value: m, label: m });
	});
</script>

<div class="parameters">
	<h4 class="select-label">&nbsp;</h4>
	<Svelecte
		style="width: 280px; flex:none;"
		bind:value
		{options}
		on:change={(e) => {
			if (e.detail.value !== model) {
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
