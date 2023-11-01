<script lang="ts">
	import HomeCard from '$lib/components/home/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/home/HomeSearchBar.svelte';

	import { EntrySort, EntryTypeFilter, type ZenoService } from '$lib/zenoapi/index.js';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let searchText = '';
	let typeFilter: EntryTypeFilter = EntryTypeFilter.ALL;
	let sort: EntrySort = EntrySort.POPULAR;

	$: updateEntries(searchText, typeFilter, sort);

	function updateEntries(searchString: string, typeFilter: EntryTypeFilter, sort: EntrySort) {
		zenoClient
			.getHomeDetails({
				searchString,
				typeFilter,
				sort
			})
			.then((res) => {
				data.entries = res;
			});
	}
</script>

<HomeSearchBar bind:searchText bind:typeFilter bind:sort />
<div class="h-full content-start overflow-y-auto grid grid-cols-home gap-5">
	{#each data.entries as entry (entry.entry.name || entry.entry.name)}
		<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
	{/each}
</div>
