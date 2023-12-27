<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { svelecteRendererName } from '$lib/util/util.js';
	import type { Project, Report, ZenoService } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let report: Report;
	export let linkedProjects: Project[];

	const zenoClient = getContext('zenoClient') as ZenoService;

	function updateReportProjects(e: CustomEvent) {
		const projectUuids = e.detail.map((p: Project) => p.uuid);
		zenoClient.updateReportProjects(report.id, projectUuids);
		invalidate('app:report');
	}
</script>

<div class="mt-2 flex w-full flex-wrap items-center gap-2">
	<p class="mr-2 text-lg text-grey-dark">Linked Projects:</p>
	{#if report.editor}
		{#await zenoClient.getUserProjects() then projects}
			<Svelecte
				bind:value={report.linkedProjects}
				on:change={updateReportProjects}
				valueField="uuid"
				labelField="name"
				searchable={false}
				multiple={true}
				options={projects}
				renderer={svelecteRendererName}
			/>
		{/await}
	{:else}
		{#each linkedProjects as project}
			<button
				class="flex w-fit items-center rounded bg-primary-light px-2 py-1 transition hover:bg-primary-mid"
				on:click={() => goto(`/project/${project.uuid}/${encodeURIComponent(project.name)}`)}
			>
				<img src="/zeno-logo-small.svg" alt="Zeno logo" class="mr-1" />
				<p class="mr-1">{project.name}</p>
			</button>
		{/each}
	{/if}
</div>
