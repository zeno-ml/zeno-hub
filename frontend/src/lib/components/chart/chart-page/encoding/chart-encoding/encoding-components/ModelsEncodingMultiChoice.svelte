<script lang="ts">
	import { models } from '$lib/stores';
	import Checkbox from '@smui/checkbox';
	import { createEventDispatcher } from 'svelte';
	import MultiSelect from 'svelte-multiselect';

	export let stringValues: string[];

	let value = stringValues;

	const dispatch = createEventDispatcher<{ selected: string[] }>();

	$: dispatch('selected', value);
</script>

<div class="flex w-full flex-col">
	{#if stringValues[0] != ''}
		<MultiSelect
			bind:selected={value}
			options={$models}
			liSelectedClass="!bg-primary-light ![&>svg]:fill-primary"
			outerDivClass="!w-full !border-grey-light !py-1 !bg-white"
			liActiveOptionClass="!bg-primary-light"
		/>
	{/if}
	<div class="ml-auto flex items-center">
		<span>All Systems</span>
		<Checkbox
			checked={value[0] == ''}
			on:click={() => (value[0] === '' ? (value = []) : (value = ['']))}
		/>
	</div>
</div>
