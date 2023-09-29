<script lang="ts">
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/general/Banner.svelte';
	import Popup from '$lib/components/popups/Popup.svelte';
	import Report from '$lib/components/report/Report.svelte';
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
</script>

<button
	class="border-solid m-1 ml-0 mb-2 rounded-sm border-grey-light border shadow-sm flex flex-col hover:shadow-md items-center justify-center w-44 p-1 pr-3 pl-1"
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
