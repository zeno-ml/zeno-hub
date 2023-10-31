<script lang="ts">
	import { HomeSort, HomeTypeFilter } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Fab from '@smui/fab';
	import { Input } from '@smui/textfield';

	export let searchText;
	export let typeFilter: HomeTypeFilter;
	export let sort: HomeSort;
	export let showNewReport = false;
	export let myHub = false;

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

<div class="flex mb-6 mt-4 md:items-center justify-between md:flex-row flex-col">
	<div class="flex md:items-center md:flex-row flex-col">
		<div
			class="h-12 w-96 px-4 py-3 flex justify-center items-center border-solid rounded-lg border-grey-light border focus-within:shadow-md"
		>
			<Icon class="material-icons">search</Icon>
			<Input
				bind:value={tempSearchText}
				on:keydown={handleKeyDown}
				placeholder="Search"
				class="ml-4"
			/>
			{#if tempSearchText !== ''}
				<Fab class="ml-4 h-12" on:click={() => (tempSearchText = '')}>
					<Icon class="material-icons">clear</Icon>
				</Fab>
			{/if}
		</div>
		<div class="flex mt-2 md:mt-0">
			<Button
				class="md:ml-4 mr-2"
				variant={typeFilter === HomeTypeFilter.PROJECT ? 'raised' : 'outlined'}
				on:click={() => updateTypeFilter(HomeTypeFilter.PROJECT)}
			>
				projects
			</Button>
			<Button
				class="bg-primary-light"
				variant={typeFilter === HomeTypeFilter.REPORT ? 'raised' : 'outlined'}
				on:click={() => updateTypeFilter(HomeTypeFilter.REPORT)}
			>
				reports
			</Button>
			{#if myHub}
				<Button class="ml-2" on:click={() => (showNewReport = true)}>
					<Icon class="material-icons" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
						<path d={mdiPlus} />
					</Icon>
					New Report
				</Button>
			{/if}
		</div>
	</div>
	<div class="mt-2 md:mt-0">
		<select class="md:ml-4 mr-2" bind:value={sort}>
			<option value={HomeSort.RECENT}>Recent</option>
			<option value={HomeSort.POPULAR}>Popular</option>
		</select>
	</div>
</div>
