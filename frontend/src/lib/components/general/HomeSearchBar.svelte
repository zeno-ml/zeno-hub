<script lang="ts">
	import { HomeSort, HomeTypeFilter } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Paper from '@smui/paper';
	import { Input } from '@smui/textfield';

	export let searchText;
	export let typeFilter: HomeTypeFilter;
	export let sort: HomeSort;

	let tempSearchText = searchText;

	$: updateSearchText(tempSearchText);

	let timer: ReturnType<typeof setTimeout>;
	function updateSearchText(text: string) {
		clearTimeout(timer);
		timer = setTimeout(() => {
			searchText = text;
		}, 200);
	}

	function updateTypeFilter(type: HomeTypeFilter) {
		if (typeFilter === type) {
			typeFilter = HomeTypeFilter.ALL;
		} else {
			typeFilter = type;
		}
	}

	function handleKeyDown(e: unknown) {
		const keyboardEvent = e as KeyboardEvent;
		// run doSearch on enter
		if (keyboardEvent.key === 'Enter') {
			doSearch();
		}
	}

	function doSearch() {}
</script>

<div class="flex mb-6 items-center justify-between">
	<div class="flex items-center">
		<Paper class="h-12 w-96 px-4 py-3 flex justify-center items-center" elevation={2}>
			<Icon class="material-icons">search</Icon>
			<Input
				bind:value={tempSearchText}
				on:keydown={handleKeyDown}
				placeholder="Search"
				class="ml-4"
			/>
		</Paper>
		<Button
			class="ml-4 mr-2"
			variant={typeFilter === HomeTypeFilter.PROJECT ? 'raised' : 'outlined'}
			on:click={() => updateTypeFilter(HomeTypeFilter.PROJECT)}
		>
			projects
		</Button>
		<Button
			variant={typeFilter === HomeTypeFilter.REPORT ? 'raised' : 'outlined'}
			on:click={() => updateTypeFilter(HomeTypeFilter.REPORT)}
		>
			reports
		</Button>
	</div>
	<div>
		<select class="ml-4 mr-2" bind:value={sort}>
			<option value={HomeSort.RECENT}>Recent</option>
			<option value={HomeSort.POPULAR}>Popular</option>
		</select>
	</div>
</div>
