<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap mb-6 h-full content-start">
	{#each data.publicReportDetails as reportDetails}
		<Report report={reportDetails.report} stats={reportDetails.statistics} />
	{/each}
</div>
