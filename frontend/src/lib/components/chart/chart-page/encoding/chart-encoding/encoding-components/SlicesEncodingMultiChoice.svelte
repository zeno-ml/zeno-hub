<script lang="ts">
	import { slices } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';
	import EncodingContainer from './EncodingContainer.svelte';

	export let numberValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { value: number; label: string }[] = [];
	let value: number[] = [];

	options.push({ value: -1, label: 'All instances' });
	// initial options & values
	$slices.forEach((s) => {
		options.push({ value: s.id, label: s.sliceName });
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
	<div class="flex flex-col">
		{#if value[0] != -2}
			<Svelecte
				style="width: 280px; flex:none;"
				bind:value
				{options}
				{dndzone}
				multiple
				placeholder="Select Slices..."
			/>
		{/if}
		<div class="ml-auto flex items-center">
			<span>All Slices</span>
			<Checkbox
				checked={value[0] == -2}
				on:click={() => (value[0] === -2 ? (value = []) : (value = [-2]))}
			/>
		</div>
	</div>
</EncodingContainer>
