<script lang="ts">
	import { EntrySort, EntryTypeFilter } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Fab from '@smui/fab';
	import { Input } from '@smui/textfield';
	import { createEventDispatcher } from 'svelte';
	import Spinner from '../general/Spinner.svelte';
	import Select from '../ui/Select.svelte';

	export let searchText: string;
	export let typeFilter: EntryTypeFilter;
	export let sort: EntrySort;
	export let loading = false;

	let dispatch = createEventDispatcher();
	let tempSearchText = searchText;
	let timer: ReturnType<typeof setTimeout>;

	$: updateSearchText(tempSearchText);

	function updateSearchText(text: string) {
		if (tempSearchText !== searchText) {
			clearTimeout(timer);
			timer = setTimeout(() => {
				searchText = text;
				dispatch('change');
			}, 200);
		}
	}
</script>

<div class="mb-4 flex flex-col justify-between md:flex-row md:items-center">
	<div
		class="flex h-12 w-96 items-center justify-center rounded-lg border border-solid border-grey-light px-4 py-3 focus-within:shadow-md"
	>
		<Icon class="material-icons">search</Icon>
		<Input bind:value={tempSearchText} placeholder="Search" class="ml-4" />
		{#if tempSearchText !== ''}
			<Fab
				class="ml-4 h-12"
				on:click={() => {
					tempSearchText = '';
					dispatch('change');
				}}
			>
				<Icon class="material-icons">clear</Icon>
			</Fab>
		{/if}
	</div>
	<div class="mt-4 hidden h-full items-center sm:flex md:ml-4 md:mt-0">
		{#if loading}
			<Spinner width={24} height={24} />
		{/if}
		<div class="ml-4 flex items-center">
			<p class="mr-1 text-grey-dark">Filter:</p>
			<Select
				bind:value={typeFilter}
				on:change={() => dispatch('change')}
				options={[
					{ value: EntryTypeFilter.ALL, label: 'Projects & Reports' },
					{ value: EntryTypeFilter.PROJECT, label: 'Projects' },
					{ value: EntryTypeFilter.REPORT, label: 'Reports' }
				]}
			/>
		</div>
		<div class="ml-6 flex items-center">
			<p class="mr-1 text-grey-dark">Sort:</p>
			<Select
				bind:value={sort}
				on:change={() => dispatch('change')}
				options={[
					{ value: EntrySort.RECENT, label: 'Recent' },
					{ value: EntrySort.POPULAR, label: 'Popular' }
				]}
			/>
		</div>
	</div>
</div>
