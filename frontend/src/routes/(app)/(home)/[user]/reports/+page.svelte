<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';

	export let data;

	$: ownReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName !== data.user?.name);
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
		You haven't created any reports yet. Use reports to tell stories about your AI systems.
	</Banner>
{/if}
<div class="flex flex-wrap mb-6 overflow-y-scroll h-full">
	{#each ownReports as report}
		<Report {report} deletable />
	{/each}
	{#each sharedReports as report}
		<Report {report} />
	{/each}
</div>
