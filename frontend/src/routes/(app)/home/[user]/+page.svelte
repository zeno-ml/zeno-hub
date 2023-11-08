<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeCard from '$lib/components/home/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/home/HomeSearchBar.svelte';
	import { EntrySort, EntryTypeFilter, ZenoService } from '$lib/zenoapi/index.js';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showNewReport = false;
	let searchText = '';
	let typeFilter: EntryTypeFilter = EntryTypeFilter.ALL;
	let sort: EntrySort = EntrySort.RECENT;

	$: updateEntries(searchText, typeFilter, sort);

	function updateEntries(searchString: string, typeFilter: EntryTypeFilter, sort: EntrySort) {
		zenoClient
			.getHomeDetails({
				userName: data.cognitoUser.name,
				searchString,
				typeFilter,
				sort
			})
			.then((res) => {
				data.entries = res;
			});
	}
</script>

<HomeSearchBar bind:typeFilter bind:searchText bind:sort />
<div class="grid h-full grid-cols-home content-start gap-5 overflow-y-auto">
	{#each data.entries as entry ('id' in entry.entry ? entry.entry.id : 'uuid' in entry.entry ? entry.entry.uuid : '')}
		<HomeCard entry={entry.entry} stats={entry.stats} user={data.user} />
	{/each}
</div>
{#if data.entries.length === 0}
	<Banner>
		<b>No results</b>. Check out the
		<a class="text-primary" href="https://zenoml.com/docs/intro/#creating-a-project">
			Getting Started Guide
		</a> to learn how to upload projects and create reports!
	</Banner>
	<br />
{/if}
