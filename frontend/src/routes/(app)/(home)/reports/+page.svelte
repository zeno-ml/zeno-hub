<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each data.publicReportDetails as reportDetail}
		<Report report={reportDetail.report} stats={reportDetail.statistics} user={data.user} />
	{/each}
</div>
