<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeCard from '$lib/components/home/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/home/HomeSearchBar.svelte';
	import { inViewport } from '$lib/util/viewport.js';
	import { EntrySort, EntryTypeFilter, ZenoService, type HomeEntry } from '$lib/zenoapi/index.js';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let searchText = '';
	let typeFilter: EntryTypeFilter = EntryTypeFilter.ALL;
	let sort: EntrySort = EntrySort.RECENT;
	let entries: HomeEntry[] = data.entries;
	let loading = false;

	function updateEntries(searchString: string, typeFilter: EntryTypeFilter, sort: EntrySort) {
		loading = true;
		zenoClient
			.getHomeDetails({
				userName: data.cognitoUser.name,
				searchString,
				typeFilter,
				sort,
				limit: 20
			})
			.then((res) => {
				entries = res;
				loading = false;
			});
	}

	function loadMore() {
		loading = true;
		const numProjects = entries.filter((entry) => 'uuid' in entry.entry).length;
		const numReports = entries.filter((entry) => 'id' in entry.entry).length;
		zenoClient
			.getHomeDetails({
				userName: data.cognitoUser.name,
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
	<title>My Hub | Zeno</title>
	<meta name="description" content="Your projects and reports." />
</svelte:head>

<HomeSearchBar
	bind:typeFilter
	bind:searchText
	bind:sort
	{loading}
	on:change={() => updateEntries(searchText, typeFilter, sort)}
/>
<div class="mb-4 grid h-full grid-cols-home content-start gap-5 overflow-y-auto">
	{#each entries as entry, i ('id' in entry.entry ? entry.entry.id : 'uuid' in entry.entry ? entry.entry.uuid : '')}
		{#if i === entries.length - 1}
			<div use:inViewport={loadMore}>
				<HomeCard
					entry={entry.entry}
					stats={entry.stats}
					user={data.user}
					on:deleted={() => updateEntries(searchText, typeFilter, sort)}
				/>
			</div>
		{:else}
			<HomeCard
				entry={entry.entry}
				stats={entry.stats}
				user={data.user}
				on:deleted={() => updateEntries(searchText, typeFilter, sort)}
			/>
		{/if}
	{/each}
</div>
{#if entries.length === 0}
	<Banner>
		<b>No results</b>. Check out the
		<a class="text-primary" href="https://zenoml.com/docs/intro/#creating-a-project">
			Getting Started Guide
		</a> to learn how to upload projects and create reports!
	</Banner>
	<br />
{/if}
