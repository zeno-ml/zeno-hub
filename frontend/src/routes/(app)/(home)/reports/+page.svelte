<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap mb-6 h-full content-start">
	{#each data.publicReportDetails as reportDetail}
		<Report
			report={reportDetail.report}
			stats={reportDetail.statistics}
			loggedIn={data.user !== null}
		/>
	{/each}
</div>
