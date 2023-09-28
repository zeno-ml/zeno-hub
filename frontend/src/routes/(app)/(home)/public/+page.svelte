<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let data;

	let view = 'projects';
</script>

{#if !data.user}
	<Banner>
		Welcome to <a href="https://zenoml.com">Zeno</a>! You can only see public projects and reports.
		<a href="/login">Login</a> or <a href="/signup">create an account</a> to create and view your own
		projects and reports.
	</Banner>
{/if}
<div class="p-4 mt-5 flex flex-col bg-white shadow">
	<div class="flex mb-4 h-8 ml-2">
		<Tooltip
			content={'Projects are datasets and system outputs for evaluation'}
			theme={'zeno-tooltip'}
			position="bottom"
		>
			<button
				class="text-xl mr-6 hover:text-primary
	{view === 'projects' ? 'border-b-2 border-primary' : ''}"
				on:click={() => (view = 'projects')}
			>
				Projects
			</button>
		</Tooltip>
		<Tooltip
			content={'Reports are interactive notebooks for sharing evaluation insights'}
			theme={'zeno-tooltip'}
			position="bottom"
		>
			<button
				class="text-xl mr-4 hover:text-primary {view === 'reports'
					? 'border-b-2 border-primary'
					: ''}"
				on:click={() => (view = 'reports')}
			>
				Reports
			</button>
		</Tooltip>
	</div>
	{#if view === 'projects'}
		<div class="flex flex-wrap items-start mb-6">
			{#each data.publicProjects as project}
				<Project {project} />
			{/each}
		</div>
	{:else if view === 'reports'}
		<div class="flex flex-wrap items-start mb-6">
			{#each data.publicReports as report}
				<Report {report} />
			{/each}
		</div>
	{/if}
</div>
