<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { showNewReport } from '$lib/stores.js';
	import type { ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { getContext } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let INSTANCES_PER_PAGE = 6;

	let currentProjectPage = 0;
	let lastProjectPage = Math.floor(data.numProjects / INSTANCES_PER_PAGE);

	let currentReportPage = 0;
	let lastReportPage = Math.floor(data.numReports / INSTANCES_PER_PAGE);

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
				offset: page * INSTANCES_PER_PAGE,
				limit: INSTANCES_PER_PAGE
			})
			.then((projects) => {
				data.projects = projects;
			});
	}
	function updateReports(page: number) {
		zenoClient
			.getReports({
				user: data.user?.name,
				offset: page * INSTANCES_PER_PAGE,
				limit: INSTANCES_PER_PAGE
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
	<Tooltip
		content={'Projects are datasets and system outputs for evaluation'}
		theme={'zeno-tooltip'}
		position="bottom"
	>
		<h2 class="text-2xl mr-6 text-black">Projects</h2>
	</Tooltip>
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

<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="total">
		{Math.min(currentProjectPage * INSTANCES_PER_PAGE + 1, data.numProjects)} - {Math.min(
			(currentProjectPage + 1) * INSTANCES_PER_PAGE,
			data.numProjects
		)} of {data.numProjects}
	</svelte:fragment>

	<IconButton
		class="material-icons"
		action="first-page"
		title="First page"
		on:click={() => (currentProjectPage = 0)}
		disabled={currentProjectPage === 0}>first_page</IconButton
	>
	<IconButton
		class="material-icons"
		action="prev-page"
		title="Prev page"
		on:click={() => currentProjectPage--}
		disabled={currentProjectPage === 0}>chevron_left</IconButton
	>
	<IconButton
		class="material-icons"
		action="next-page"
		title="Next page"
		on:click={() => currentProjectPage++}
		disabled={currentProjectPage >= lastProjectPage}>chevron_right</IconButton
	>
	<IconButton
		class="material-icons"
		action="last-page"
		title="Last page"
		on:click={() => (currentProjectPage = lastProjectPage)}
		disabled={currentProjectPage >= lastProjectPage}>last_page</IconButton
	>
</Pagination>

<div class="flex flex-col sm:flex-row sm:items-center mb-4 mt-6">
	<Tooltip
		content={'Reports are interactive notebooks for sharing evaluation insights'}
		theme={'zeno-tooltip'}
		position="bottom"
	>
		<p class="text-2xl mr-6 text-black">Reports</p>
	</Tooltip>
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
<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="total">
		{Math.min(currentReportPage * INSTANCES_PER_PAGE + 1, data.numReports)} - {Math.min(
			(currentReportPage + 1) * INSTANCES_PER_PAGE,
			data.numReports
		)} of {data.numReports}
	</svelte:fragment>

	<IconButton
		class="material-icons"
		action="first-page"
		title="First page"
		on:click={() => (currentReportPage = 0)}
		disabled={currentReportPage === 0}>first_page</IconButton
	>
	<IconButton
		class="material-icons"
		action="prev-page"
		title="Prev page"
		on:click={() => currentReportPage--}
		disabled={currentReportPage === 0}>chevron_left</IconButton
	>
	<IconButton
		class="material-icons"
		action="next-page"
		title="Next page"
		on:click={() => currentReportPage++}
		disabled={currentReportPage >= lastReportPage}>chevron_right</IconButton
	>
	<IconButton
		class="material-icons"
		action="last-page"
		title="Last page"
		on:click={() => (currentReportPage = lastReportPage)}
		disabled={currentReportPage >= lastReportPage}>last_page</IconButton
	>
</Pagination>
<br class="mt-20" />
