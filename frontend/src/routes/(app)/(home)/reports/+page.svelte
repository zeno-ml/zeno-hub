<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap items-start mb-6">
	{#each data.publicReports as report}
		<Report {report} />
	{/each}
</div>
