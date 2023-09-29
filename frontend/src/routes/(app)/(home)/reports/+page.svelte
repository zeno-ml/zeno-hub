<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap justify-start mb-6 overflow-y-scroll h-full">
	{#each data.publicReports as report}
		<Report {report} />
	{/each}
</div>
