<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap mb-6 h-full content-start">
	{#each data.publicReports as report}
		<Report report={report.report} stats={report.statistics} loggedIn={data.user !== null} />
	{/each}
</div>
