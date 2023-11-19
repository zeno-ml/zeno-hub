<script lang="ts">
	import HomeCard from '$lib/components/home/HomeCard.svelte';
	import type { Project, Report } from '$lib/zenoapi/index.js';

	export let data;

	function getUrl(entry: Report | Project) {
		return `https://hub.zenoml.com/${'uuid' in entry ? 'project' : 'report'}/${
			'uuid' in entry ? entry.uuid : entry.id
		}/${encodeURIComponent(entry.name)}`;
	}
</script>

<div class="grid h-full grid-cols-home content-start gap-5 overflow-x-auto">
	{#each data.entries as entry (entry.entry.name || entry.entry.name)}
		<div class="relative">
			<HomeCard entry={entry.entry} stats={entry.stats} user={null} />
			<a
				href={getUrl(entry.entry)}
				target="_blank"
				class="absolute bottom-0 left-0 right-0 top-0 z-20 rounded-lg shadow-sm hover:shadow-md"
			>
			</a>
		</div>
	{/each}
</div>
