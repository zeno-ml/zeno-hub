<script lang="ts">
	import HomePagination from '$lib/components/general/HomePagination.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import type { ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const ENTRIES_PER_PAGE = 6;

	let currentProjectPage = 0;
	let currentReportPage = 0;

	$: updateProjects(currentProjectPage);
	$: updateReports(currentReportPage);

	function updateProjects(page: number) {
		zenoClient
			.getProjects({
				offset: page * ENTRIES_PER_PAGE,
				limit: ENTRIES_PER_PAGE
			})
			.then((projects) => {
				data.projects = projects;
			});
	}

	function updateReports(page: number) {
		zenoClient
			.getReports({
				offset: page * ENTRIES_PER_PAGE,
				limit: ENTRIES_PER_PAGE
			})
			.then((reports) => {
				data.reports = reports;
			});
	}
</script>

<div class="flex flex-col sm:flex-row sm:items-center mb-4">
	<h2 class="text-2xl mr-6 text-black">Projects</h2>
	<p class="text-lg ml-1 text-grey-dark">
		Explore, evaluate, and visualize AI systems.
		<a class="text-primary" href="http://zenoml.com">Learn more!</a>
	</p>
</div>
<div class="h-full grid-cols-home grid gap-3">
	{#each data.projects as project, i}
		<Project {project} stats={data.projectsStats[i]} user={data.user} />
	{/each}
</div>
<HomePagination
	bind:currentPage={currentProjectPage}
	totalEntries={data.numProjects}
	{ENTRIES_PER_PAGE}
/>

<div class="flex flex-col sm:flex-row sm:items-center mb-4">
	<p class="text-2xl mr-6 text-black">Reports</p>
	<p class="text-lg ml-1 text-grey-dark">
		Author interactive, data-driven AI evaluation reports.
		<a class="text-primary" href="http://zenoml.com">Learn more!</a>
	</p>
</div>
<div class="h-full grid-cols-home grid gap-3">
	{#each data.reports as report, i}
		<Report {report} stats={data.reportsStats[i]} loggedIn={data.user !== null} />
	{/each}
</div>
<HomePagination
	bind:currentPage={currentReportPage}
	totalEntries={data.numReports}
	{ENTRIES_PER_PAGE}
/>

<br class="mt-20" />
