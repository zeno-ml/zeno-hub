<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeCardsContainer from '$lib/components/general/HomeCardsContainer.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';

	export let data;
</script>

{#if $showNewReport && data.user !== null}
	<NewReportPopup
		on:close={() => {
			showNewReport.set(false);
		}}
		user={data.user.name}
		reports={data.reports}
	/>
{/if}
{#if data.reports.length === 0}
	<Banner>
		You haven't created any reports yet. Use charts from your projects to create interactive
		reports.
	</Banner>
{/if}
<HomeCardsContainer>
	{#each data.reports as report, i}
		<Report {report} stats={data.statistics[i]} user={data.user} deletable />
	{/each}
</HomeCardsContainer>
