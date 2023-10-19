<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';

	export let data;

	$: ownReports =
		data.user === null
			? []
			: data.reports.filter((rep) => rep.report.ownerName === data.user?.name);
	$: sharedReports =
		data.user === null
			? []
			: data.reports.filter((rep) => rep.report.ownerName !== data.user?.name);
</script>

{#if $showNewReport && data.user !== null}
	<NewReportPopup
		on:close={() => {
			showNewReport.set(false);
		}}
		user={data.user.name}
		reports={ownReports.map((r) => r.report)}
	/>
{/if}
{#if ownReports.length === 0}
	<Banner>
		You haven't created any reports yet. Use charts from your projects to create interactive
		reports.
	</Banner>
{/if}
<div class="flex flex-wrap mb-6 h-full content-start">
	{#each ownReports as report}
		<Report
			report={report.report}
			stats={report.statistics}
			loggedIn={data.user !== null}
			deletable
		/>
	{/each}
	{#each sharedReports as report}
		<Report report={report.report} stats={report.statistics} loggedIn={data.user !== null} />
	{/each}
</div>
