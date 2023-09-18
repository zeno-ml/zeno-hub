<script lang="ts">
	import { goto } from '$app/navigation';
	import Popup from '$lib/components/popups/Popup.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { featureFlags } from '$lib/stores.js';
	import { ZenoService } from '$lib/zenoapi/index.js';
	import { mdiPlus } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';

	export let data;

	let reportName = '';
	let showNewReport = false;

	$: invalidName = data.reports.filter((rep) => rep.name === reportName).length > 0;

	$: ownReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName !== data.user?.name);
	$: publicReports = data.publicReports.filter(
		(rep) =>
			ownReports.find((own) => own.id === rep.id) === undefined &&
			sharedReports.find((shared) => shared.id === rep.id) === undefined
	);

	$: ownProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName !== data.user?.name);
	$: publicProjects = data.publicProjects.filter(
		(proj) =>
			ownProjects.find((own) => own.uuid === proj.uuid) === undefined &&
			sharedProjects.find((shared) => shared.uuid === proj.uuid) === undefined
	);
</script>

<div class="p-4 w-full bg-yellowish overflow-x-scroll">
	<div class="flex flex-col bg-white p-6 shadow-md rounded mb-4">
		{#if data.user}
			{#if ownProjects.length > 0}
				<h1 class="text-xl mb-4">Your projects</h1>
				<div class="flex flex-wrap items-start">
					{#each ownProjects as project}
						<Project {project} deletable />
					{/each}
				</div>
			{:else if $featureFlags['WELCOME_TEXT']}
				<p class="text-lg mt-3 mb-4">
					Welcome to Zeno! You don't have any projects yet. Create one with the <a
						href="https://github.com/zeno-ml/zeno-client">Zeno Client.</a
					>
				</p>
			{/if}
			{#if sharedProjects.length > 0}
				<h1 class="text-xl mt-3 mb-4">Shared Projects</h1>
				<div class="flex flex-wrap items-start">
					{#each sharedProjects as project}
						<Project {project} />
					{/each}
				</div>
			{/if}
		{/if}
		{#if publicProjects.length > 0}
			<h1 class="text-xl mt-3 mb-4">Public Projects</h1>
			<div class="flex flex-wrap items-start">
				{#each publicProjects as project}
					<Project {project} />
				{/each}
			</div>
		{/if}
		{#if !data.user && $featureFlags['WELCOME_TEXT']}
			<p class="text-lg mt-3 ml-1">
				Welcome to Zeno! You can only see public projects. <a href="/login">Login</a> or
				<a href="/signup">create an account</a> to see your own projects.
			</p>
		{/if}
	</div>
	{#if $featureFlags['REPORTS']}
		<div class="flex flex-col bg-white p-6 shadow-md rounded">
			{#if data.user}
				<div class="flex items-center mb-4">
					<h1 class="text-xl mr-4">Your Reports</h1>
					<button
						class="border-solid m-1 rounded-sm border-grey-light border shadow-sm flex flex-col hover:shadow-md p-1 pr-3 pl-1"
						on:click={() => (showNewReport = true)}
					>
						<div class="flex items-center">
							<Icon
								class="mr-2"
								style="outline:none;"
								width="24px"
								height="24px"
								tag="svg"
								viewBox="0 0 24 24"
							>
								<path fill="black" d={mdiPlus} />
							</Icon>
							New Report
						</div>
					</button>
				</div>
				<div class="flex flex-wrap items-start">
					{#each ownReports as report}
						<Report {report} deletable />
					{/each}
				</div>
				{#if sharedReports.length > 0}
					<h1 class="text-xl mt-3 mb-4">Shared Reports</h1>
					<div class="flex flex-wrap items-start">
						{#each sharedReports as report}
							<Report {report} />
						{/each}
					</div>
				{/if}
			{/if}
			{#if publicReports.length > 0}
				<h1 class="text-xl mt-3 mb-4">Public Reports</h1>
				<div class="flex flex-wrap items-start">
					{#each publicReports as report}
						<Report {report} />
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>
{#if showNewReport}
	<Popup on:close>
		<Content style="display: flex; align-items: center;">
			<Textfield bind:value={reportName} label="Report Name" />
			<Button
				style="margin-left: 10px;"
				variant="outlined"
				on:click={() => (showNewReport = false)}
			>
				Cancel
			</Button>
			<Button
				style="margin-left: 5px;"
				variant="outlined"
				disabled={invalidName}
				on:click={() => {
					{
						ZenoService.addReport(reportName).then(() =>
							goto(`/report/${data.user?.name}/${reportName}`)
						);
					}
				}}
			>
				Create
			</Button>
		</Content>
		{#if invalidName && reportName.length > 0}
			<p style:margin-right="10px" style:color="red">report already exists</p>
		{/if}
	</Popup>
{/if}
