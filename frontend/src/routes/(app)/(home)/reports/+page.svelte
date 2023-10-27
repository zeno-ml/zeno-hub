<script lang="ts">
	import HomeCardsContainer from '$lib/components/general/HomeCardsContainer.svelte';
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

<HomeCardsContainer>
	{#each data.reports as report, i}
		<Report {report} stats={data.statistics[i]} user={data.user} />
	{/each}
</HomeCardsContainer>
