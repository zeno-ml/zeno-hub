<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';

	export let data;
</script>

{#if !data.user}
	<Banner>
		Welcome to Zeno! You can only see public projects and reports.
		<a href="/login">Login</a> or <a href="/signup">create an account</a> to create and view your own
		projects and reports.
	</Banner>
{/if}
<div class="pt-8 flex flex-col">
	{#if data.publicProjects.length > 0}
		<h1 class="text-xl mb-4">Projects</h1>
		<div class="flex flex-wrap items-start mb-6">
			{#each data.publicProjects as project}
				<Project {project} />
			{/each}
		</div>
	{/if}
	{#if data.publicReports.length > 0}
		<h1 class="text-xl mb-4">Reports</h1>
		<div class="flex flex-wrap items-start mb-6">
			{#each data.publicReports as report}
				<Report {report} />
			{/each}
		</div>
	{/if}
</div>
