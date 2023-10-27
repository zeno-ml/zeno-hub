<script lang="ts">
	import { models } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';
	import EncodingContainer from './EncodingContainer.svelte';

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

<EncodingContainer>
	<div class="flex flex-col">
		{#if value[0] != 'all_zeno_project_models'}
			<Svelecte
				style="width: 280px; flex:none;"
				bind:value
				{options}
				{dndzone}
				multiple
				placeholder="Select Slices..."
			/>
		{/if}
		<div class="flex items-center ml-auto">
			<span>All Models</span>
			<Checkbox
				checked={value[0] == 'all_zeno_project_models'}
				on:click={() =>
					value[0] === 'all_zeno_project_models'
						? (value = [])
						: (value = ['all_zeno_project_models'])}
			/>
		</div>
	</div>
</EncodingContainer>
