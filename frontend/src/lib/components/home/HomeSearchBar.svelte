<script lang="ts">
	import { EntrySort, EntryTypeFilter } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Fab from '@smui/fab';
	import { Input } from '@smui/textfield';

	export let searchText;
	export let typeFilter: EntryTypeFilter;
	export let sort: EntrySort;

	let tempSearchText = searchText;
	let timer: ReturnType<typeof setTimeout>;

	$: updateSearchText(tempSearchText);

	function updateSearchText(text: string) {
		clearTimeout(timer);
		timer = setTimeout(() => {
			searchText = text;
		}, 200);
	}
</script>

<div class="mb-4 mt-4 flex flex-col justify-between md:flex-row md:items-center">
	<div
		class="flex h-12 w-96 items-center justify-center rounded-lg border border-solid border-grey-light px-4 py-3 focus-within:shadow-md"
	>
		<Icon class="material-icons">search</Icon>
		<Input bind:value={tempSearchText} placeholder="Search" class="ml-4" />
		{#if tempSearchText !== ''}
			<Fab class="ml-4 h-12" on:click={() => (tempSearchText = '')}>
				<Icon class="material-icons">clear</Icon>
			</Fab>
		{/if}
	</div>
	<div class="mt-4 flex h-full items-center md:ml-4 md:mt-0">
		<div class="ml-4 flex items-center">
			<p class="mr-1 text-grey-dark">Filter:</p>
			<select class="h-full px-2" bind:value={typeFilter}>
				<option value={EntryTypeFilter.ALL}>Projects & Reports</option>
				<option value={EntryTypeFilter.PROJECT}>Projects</option>
				<option value={EntryTypeFilter.REPORT}>Reports</option>
			</select>
		</div>
		<div class="ml-6 flex items-center">
			<p class="mr-1 text-grey-dark">Sort:</p>
			<select class="h-full px-2" bind:value={sort}>
				<option value={EntrySort.RECENT}>Recent</option>
				<option value={EntrySort.POPULAR}>Popular</option>
			</select>
		</div>
	</div>
</div>
