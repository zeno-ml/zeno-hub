<script lang="ts">
	import Spinner from '$lib/components/general/Spinner.svelte';
	import HomeCard from '$lib/components/home/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/home/HomeSearchBar.svelte';
	import { inViewport } from '$lib/util/viewport';

	import {
		EntrySort,
		EntryTypeFilter,
		type HomeEntry,
		type ZenoService
	} from '$lib/zenoapi/index.js';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let searchText = '';
	let typeFilter: EntryTypeFilter = EntryTypeFilter.ALL;
	let sort: EntrySort = EntrySort.POPULAR;
	let entries: HomeEntry[] = data.entries;
	let loading = false;

	function updateEntries(searchString: string, typeFilter: EntryTypeFilter, sort: EntrySort) {
		zenoClient
			.getHomeDetails({
				searchString,
				typeFilter,
				sort,
				limit: 20
			})
			.then((res) => {
				entries = res;
			});
	}

	function loadMore() {
		loading = true;
		const numProjects = entries.filter((entry) => 'uuid' in entry.entry).length;
		const numReports = entries.filter((entry) => 'id' in entry.entry).length;
		zenoClient
			.getHomeDetails({
				searchString: searchText,
				typeFilter,
				sort,
				projectOffset: numProjects,
				reportOffset: numReports,
				limit: 20
			})
			.then((res) => {
				entries = [...entries, ...res];
				loading = false;
			});
	}
</script>

<svelte:head>
	<title>Explore | Zeno</title>
	<meta name="description" content="Explore public evaluation projects and reports." />
</svelte:head>

<HomeSearchBar
	bind:searchText
	bind:typeFilter
	bind:sort
	on:change={() => updateEntries(searchText, typeFilter, sort)}
/>
<div class="mb-4 grid h-full grid-cols-home content-start gap-5 overflow-y-auto">
	{#each entries as entry, i ('id' in entry.entry ? entry.entry.id : 'uuid' in entry.entry ? entry.entry.uuid : '')}
		{#if i === entries.length - 1}
			<div use:inViewport={loadMore}>
				<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
			</div>
		{:else}
			<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
		{/if}
	{/each}
	{#if loading}
		<Spinner width={24} height={24} />
	{/if}
</div>
