<script lang="ts">
	import { metrics } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import { createEventDispatcher } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';

	export let numberValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { value: number; label: string }[] = [];
	let value: { value: number; label: string }[] = [];

	// initial options & values
	options.push({ value: -1, label: 'slice size' });
	$metrics.forEach((m) => {
		options.push({ value: m.id, label: m.name });
	});
	value = numberValues.map((v) => {
		return { value: v, label: options.find((o) => o.value === v)?.label || '' };
	});

	function updateDragOrder(val: { value: number; label: string }[]) {
		dispatch(
			'selected',
			val.map((v) => v.value)
		);
	}

	$: updateDragOrder(value);
</script>

<div class="flex flex-col">
	{#if value[0].value != -2}
		<MultiSelect
			bind:selected={value}
			{options}
			liSelectedClass="!bg-primary-light ![&>svg]:fill-primary"
			outerDivClass="!w-full !border-grey-light !py-1 !bg-white"
			liActiveOptionClass="!bg-primary-light"
		/>
	{/if}
	<div class="ml-auto flex items-center">
		<span>All Metrics</span>
		<Checkbox
			checked={value[0].value == -2}
			on:click={() =>
				value[0].value === -2 ? (value = []) : (value = [{ value: -1, label: 'slice size' }])}
		/>
	</div>
</div>
