<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each data.reports as report, i}
		<Report {report} stats={data.statistics[i]} loggedIn={data.user !== null} />
	{/each}
</div>
