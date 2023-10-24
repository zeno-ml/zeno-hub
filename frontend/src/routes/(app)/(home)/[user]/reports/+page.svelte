<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';

	export let data;

	$: ownReports = data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports = data.reports.filter((rep) => rep.ownerName !== data.user?.name);
</script>

{#if $showNewReport && data.user !== null}
	<NewReportPopup
		on:close={() => {
			showNewReport.set(false);
		}}
		user={data.user.name}
		reports={ownReports}
	/>
{/if}
{#if ownReports.length === 0}
	<Banner>
		You haven't created any reports yet. Use charts from your projects to create interactive
		reports.
	</Banner>
{/if}
<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each ownReports as report, i}
		<Report {report} stats={data.statistics[i]} loggedIn deletable />
	{/each}
	{#each sharedReports as report, i}
		<Report {report} stats={data.statistics[i]} loggedIn />
	{/each}
</div>
