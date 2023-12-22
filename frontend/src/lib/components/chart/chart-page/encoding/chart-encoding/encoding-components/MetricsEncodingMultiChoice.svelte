<script lang="ts">
	import { metrics } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import { createEventDispatcher } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';

	export let numberValues: number[];

	const dispatch = createEventDispatcher<{ selected: number[] }>();

	let options: { id: number; label: string }[] = [];
	let selected: { id: number; label: string }[] = [];

	// initial options & values
	options.push({ id: -1, label: 'slice size' });
	$metrics.forEach((m) => {
		options.push({ id: m.id, label: m.name });
	});
	selected = numberValues.map((v) => {
		return { id: v, label: options.find((o) => o.id === v)?.label || '' };
	});

	$: dispatch(
		'selected',
		selected.map((v) => v.id)
	);
</script>

<div class="flex flex-col">
	{#if selected.length === 0 || selected[0].id != -2}
		<MultiSelect
			bind:selected
			{options}
			key={JSON.stringify}
			liSelectedClass="!bg-primary-light ![&>svg]:fill-primary"
			outerDivClass="!w-full !border-grey-light !py-1 !bg-white"
			liActiveOptionClass="!bg-primary-light"
		>
			<p class="text-pretty" slot="selected" let:option>{option.label}</p>
		</MultiSelect>
	{/if}
	<div class="ml-auto flex items-center">
		<span>All Metrics</span>
		<!-- An ID of -2 indicates "all metrics". -->
		<Checkbox
			checked={selected.length > 0 && selected[0].id == -2}
			on:click={() =>
				selected.length > 0 && selected[0].id === -2
					? (selected = [])
					: (selected = [{ id: -2, label: '' }])}
		/>
	</div>
</div>
