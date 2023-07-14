<script lang="ts">
	import { slices } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let currentValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { value: number; label: string }[] = [];
	let value: number[] = [];

	// initial options & values
	$slices.forEach((s) => {
		options.push({ value: s.id, label: s.sliceName });
	});
	value = currentValues;

	function updateDragOrder(val: number[]) {
		// check if all elements are numbers (dndzone's place holder)
		if (!val.some((i) => !Number.isInteger(i))) {
			dispatch('selected', val);
		}
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
