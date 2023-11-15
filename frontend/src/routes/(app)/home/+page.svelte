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

<svelte:head>
	<title>Explore | Zeno</title>
	<meta name="description" content="Explore public evaluation projects and reports." />
</svelte:head>

<HomeSearchBar bind:searchText bind:typeFilter bind:sort />
<div class="grid h-full grid-cols-home content-start gap-5 overflow-y-auto">
	{#each data.entries as entry ('id' in entry.entry ? entry.entry.id : 'uuid' in entry.entry ? entry.entry.uuid : '')}
		<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
	{/each}
</div>
