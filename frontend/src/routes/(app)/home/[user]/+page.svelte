<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeCard from '$lib/components/general/HomeCard.svelte';
	import HomeSearchBar from '$lib/components/general/HomeSearchBar.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import { HomeSort, HomeTypeFilter, ZenoService } from '$lib/zenoapi/index.js';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showNewReport = false;
	let searchText = '';
	let typeFilter: HomeTypeFilter = HomeTypeFilter.ALL;
	let sort: HomeSort = HomeSort.RECENT;

	$: updateEntries(searchText, typeFilter, sort);

	function updateEntries(searchString: string, typeFilter: HomeTypeFilter, sort: HomeSort) {
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

{#if showNewReport && data.user !== null}
	<NewReportPopup
		on:close={() => (showNewReport = false)}
		user={data.user.name}
		bind:showNewReport
	/>
{/if}

<HomeSearchBar bind:typeFilter bind:searchText bind:sort />
<Button on:click={() => (showNewReport = true)}>
	<Icon class="material-icons" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
		<path d={mdiPlus} />
	</Icon>
	New Report
</Button>
<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each data.entries as entry (entry.entry.name || entry.entry.name)}
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
