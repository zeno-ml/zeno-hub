<script lang="ts">
	import { slices } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import { createEventDispatcher } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';

	export let numberValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { value: number; label: string }[] = [];
	let value: { value: number; label: string }[] = [];

	options.push({ value: -1, label: 'All instances' });
	// initial options & values
	$slices.forEach((s) => {
		options.push({ value: s.id, label: s.sliceName });
	});
	value = numberValues.map((v) => {
		return { value: v, label: options.find((o) => o.value === v)?.label || '' };
	});

	function updateDragOrder(val: { value: number; label: string }[]) {
		console.log(value);
		dispatch(
			'selected',
			val.map((v) => v.value)
		);
	}

	$: updateDragOrder(value);
</script>

<div class="flex flex-col">
	{#if value.length === 0 || value[0].value != -2}
		<MultiSelect
			bind:selected={value}
			{options}
			liSelectedClass="!bg-primary-light ![&>svg]:fill-primary"
			outerDivClass="!w-full !border-grey-light !py-1 !bg-white"
			liActiveOptionClass="!bg-primary-light"
		/>
	{/if}
	<div class="ml-auto flex items-center">
		<span>All Slices</span>
		<Checkbox
			checked={value.length > 0 && value[0].value == -2}
			on:click={() =>
				value.length > 0 && value[0].value === -2
					? (value = [])
					: (value = [{ value: -2, label: '' }])}
		/>
	</div>
</div>
