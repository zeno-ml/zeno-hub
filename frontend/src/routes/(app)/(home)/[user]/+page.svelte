<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomePagination from '$lib/components/general/HomePagination.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';
	import type { ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const ENTRIES_PER_PAGE = 6;

	let currentProjectPage = 0;
	let currentReportPage = 0;

	$: updateProjects(currentProjectPage);
	$: updateReports(currentReportPage);

	$: ownReports = data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports = data.reports.filter((rep) => rep.ownerName !== data.user?.name);

	$: ownProjects = data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects = data.projects.filter((proj) => proj.ownerName !== data.user?.name);

	function updateProjects(page: number) {
		zenoClient
			.getProjects({
				user: data.user?.name,
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
				user: data.user?.name,
				offset: page * ENTRIES_PER_PAGE,
				limit: ENTRIES_PER_PAGE
			})
			.then((reports) => {
				data.reports = reports;
			});
	}
</script>

{#if $showNewReport && data.user !== null}
	<NewReportPopup
		on:close={() => {
			showNewReport.set(false);
		}}
		user={data.user.name}
		reports={ownReports}
	/>
{/if}
<div class="flex flex-col sm:flex-row sm:items-center mb-3">
	<h2 class="text-2xl mr-6 text-black">Projects</h2>
	<p class="italic text-lg ml-1 text-grey-dark">
		Explore, evaluate, and visualize AI systems with Zeno Projects.
		<a class="text-primary" href="http://zenoml.com">Learn more!</a>
	</p>
</div>
{#if ownProjects.length === 0}
	<Banner>
		Welcome to <a class="text-primary" href="https://zenoml.com">Zeno</a>! You haven't created any
		projects yet. Check out the
		<a class="text-primary" href="https://zenoml.com/docs/intro/#creating-a-project">
			Getting Started Guide
		</a>!
	</Banner>
	<br />
{/if}
<div class="mb-6 h-full grid-cols-home grid gap-3">
	{#each ownProjects as project, i}
		<Project {project} stats={data.projectsStats[i]} user={data.user} deletable />
	{/each}
	{#each sharedProjects as project, i}
		<Project {project} stats={data.projectsStats[i]} user={data.user} />
	{/each}
</div>
<HomePagination
	bind:currentPage={currentProjectPage}
	totalEntries={data.numProjects}
	{ENTRIES_PER_PAGE}
/>

<div class="flex flex-col sm:flex-row sm:items-center mb-4 mt-6">
	<p class="text-2xl mr-6 text-black">Reports</p>
	<p class="text-lg ml-1 text-grey-dark">
		Author interactive, data-driven AI evaluation reports.
		<a class="text-primary" href="http://zenoml.com">Learn more!</a>
	</p>
	{#if data.user}
		<div class="ml-auto mr-2">
			<Button on:click={() => showNewReport.set(true)}>
				<Icon class="material-icons" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
					<path d={mdiPlus} />
				</Icon>
				New Report
			</Button>
		</div>
	{/if}
</div>
{#if ownReports.length === 0}
	<Banner>
		You haven't created any reports yet. Use charts from your projects to create interactive
		reports.
	</Banner>
{/if}
<div class="h-full grid-cols-home grid gap-3">
	{#each ownReports as report, i}
		<Report {report} stats={data.reportsStats[i]} loggedIn deletable />
	{/each}
	{#each sharedReports as report, i}
		<Report {report} stats={data.reportsStats[i]} loggedIn />
	{/each}
</div>
<HomePagination
	bind:currentPage={currentReportPage}
	totalEntries={data.numReports}
	{ENTRIES_PER_PAGE}
/>
<br class="mt-20" />
