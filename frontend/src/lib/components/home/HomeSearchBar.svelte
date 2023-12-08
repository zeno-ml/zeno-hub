<script lang="ts">
	import { EntrySort, EntryTypeFilter } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Fab from '@smui/fab';
	import { Input } from '@smui/textfield';
	import { createEventDispatcher } from 'svelte';
	import Spinner from '../general/Spinner.svelte';

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
	<div class="mt-4 flex h-full items-center md:ml-4 md:mt-0">
		{#if loading}
			<Spinner width={24} height={24} />
		{/if}
		<div class="ml-4 flex items-center">
			<p class="mr-1 text-grey-dark">Filter:</p>
			<select class="h-full px-2" bind:value={typeFilter} on:change={() => dispatch('change')}>
				<option value={EntryTypeFilter.ALL}>Projects & Reports</option>
				<option value={EntryTypeFilter.PROJECT}>Projects</option>
				<option value={EntryTypeFilter.REPORT}>Reports</option>
			</select>
		</div>
		<div class="ml-6 flex items-center">
			<p class="mr-1 text-grey-dark">Sort:</p>
			<select class="h-full px-2" bind:value={sort} on:change={() => dispatch('change')}>
				<option value={EntrySort.RECENT}>Recent</option>
				<option value={EntrySort.POPULAR}>Popular</option>
			</select>
		</div>
	</div>
</div>
