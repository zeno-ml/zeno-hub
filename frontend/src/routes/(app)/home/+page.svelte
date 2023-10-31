<script lang="ts">
	import HomeCard from '$lib/components/general/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/general/HomeSearchBar.svelte';

	import { HomeSort, HomeTypeFilter, type ZenoService } from '$lib/zenoapi/index.js';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let searchText = '';
	let typeFilter: HomeTypeFilter = HomeTypeFilter.ALL;
	let sort: HomeSort = HomeSort.POPULAR;

	$: updateEntries(searchText, typeFilter, sort);

	function updateEntries(searchString: string, typeFilter: HomeTypeFilter, sort: HomeSort) {
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
<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each data.entries as entry (entry.entry.name || entry.entry.name)}
		<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
	{/each}
</div>
