<script lang="ts">
	import { models } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let stringValues: string[];

	const dispatch = createEventDispatcher<{ selected: string[] }>();

	let options: { value: string; label: string }[] = [];
	let value: string[] = [];

	// initial options & values
	$models.forEach((m) => {
		options.push({ value: m, label: m });
	});
	value = stringValues;

	function updateDragOrder(val: string[]) {
		// check if all elements are numbers (dndzone's place holder)
		dispatch('selected', val);
	}

	$: updateDragOrder(value);
</script>

<div class="parameters">
	<h4 class="select-label">&nbsp;</h4>
	<Svelecte
		style="width: 280px; flex:none;"
		bind:value
		{options}
		{dndzone}
		multiple
		placeholder="Select Slices..."
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

	:global(#dnd-action-dragged-el .sv-item) {
		--sv-item-selected-bg: var(--P3);
		--sv-item-btn-bg: var(--P3);
	}
	:global(div[role='listitem']) {
		outline: none;
	}
</style>
