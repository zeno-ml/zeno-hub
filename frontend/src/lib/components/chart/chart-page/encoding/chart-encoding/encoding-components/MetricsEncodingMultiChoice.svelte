<script lang="ts">
	import { metrics } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';
	import EncodingContainer from './EncodingContainer.svelte';

	export let numberValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { value: number; label: string }[] = [];
	let value: number[] = [];

	// initial options & values
	$metrics.forEach((m) => {
		options.push({ value: m.id, label: m.name });
	});
	value = numberValues;

	function updateDragOrder(val: number[]) {
		// check if all elements are numbers (dndzone's place holder)
		if (!val.some((i) => !Number.isInteger(i))) {
			dispatch('selected', val);
		}
	}

	$: updateDragOrder(value);
</script>

<EncodingContainer>
	<Svelecte
		style="width: 280px; flex:none;"
		bind:value
		{options}
		{dndzone}
		multiple={true}
		placeholder="Select Metrics..."
	/>
</EncodingContainer>
