<script lang="ts">
	import HomeCard from '$lib/components/home/HomeCard.svelte';

	export let data;
</script>

<div class="grid h-full grid-cols-home content-start gap-5 overflow-x-auto">
	{#each data.entries as entry (entry.entry.name || entry.entry.name)}
		<div class="relative">
			<HomeCard entry={entry.entry} stats={entry.stats} user={null} />
			<a
				href="https://hub.zenoml.com/{'uuid' in entry.entry ? 'project' : 'report'}/{entry.entry
					.ownerName}/{entry.entry.name}"
				target="_blank"
				class="absolute bottom-0 left-0 right-0 top-0 z-20 rounded-lg shadow-sm hover:shadow-md"
			>
			</a>
		</div>
	{/each}
</div>
