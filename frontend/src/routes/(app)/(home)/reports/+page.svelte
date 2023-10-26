<script lang="ts">
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<div class="h-full overflow-y-auto grid grid-cols-home gap-4">
	{#each data.reports as report, i}
		<Report {report} stats={data.statistics[i]} user={data.user} />
	{/each}
</div>
