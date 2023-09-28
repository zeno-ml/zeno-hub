<script lang="ts">
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/general/Banner.svelte';
	import Popup from '$lib/components/popups/Popup.svelte';
	import Project from '$lib/components/project/Project.svelte';
	import Report from '$lib/components/report/Report.svelte';
	import { ZenoService } from '$lib/zenoapi/index.js';
	import { mdiPlus } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let data;

	let reportName = '';
	let showNewReport = false;
	let view = 'projects';

	$: invalidName = data.reports.filter((rep) => rep.name === reportName).length > 0;

	$: ownReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName !== data.user?.name);

	$: ownProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName !== data.user?.name);
</script>

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
		{#if view === 'reports'}
			<button
				class="border-solid m-1 rounded-sm border-grey-light border shadow-sm flex flex-col hover:shadow-md items-center justify-center"
				on:click={() => (showNewReport = true)}
			>
				<div class="flex items-center px-3">
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
		{/if}
	</div>
	{#if view === 'projects'}
		<div class="flex flex-wrap items-start mb-6">
			{#each ownProjects as project}
				<Project {project} deletable />
			{/each}
			{#each sharedProjects as project}
				<Project {project} />
			{/each}
		</div>
		{#if ownProjects.length === 0}
			<Banner>
				Welcome to <a href="https://zenoml.com">Zeno</a>! You don't have any projects yet. Create
				one with the <a href="https://github.com/zeno-ml/zeno-client">Zeno Client.</a>
			</Banner>
		{/if}
	{:else if view === 'reports'}
		<div class="flex flex-wrap items-start mb-6">
			{#each ownReports as report}
				<Report {report} deletable />
			{/each}
			{#each sharedReports as report}
				<Report {report} />
			{/each}
		</div>
		{#if ownReports.length === 0}
			<Banner>
				You haven't created any reports yet. Use reports to tell stories about your AI systems.
			</Banner>
		{/if}
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
