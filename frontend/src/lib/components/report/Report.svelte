<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import ProjectStat from '$lib/components/project/ProjectStat.svelte';
	import { clickOutside } from '$lib/util/clickOutside';
	import { shortenNumber } from '$lib/util/util';
	import { ZenoService, type Report } from '$lib/zenoapi';
	import { mdiDotsHorizontal, mdiFileTree, mdiSitemap } from '@mdi/js';
	import { Icon } from '@smui/button';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let report: Report;
	export let deletable = false;

	let showOptions = false;
	let hovering = false;
</script>

<button
	on:click={() => goto(`/report/${report.ownerName}/${report.name}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="border-solid mr-2 rounded-lg border-grey-light border shadow-sm flex flex-col p-3 px-5 hover:shadow-md w-80 h-60"
>
	<div class="flex flex-col w-full">
		<div class="flex justify-between items-center">
			<p class="text-black text-lg mr-2">{report.name}</p>
			<div
				class="w-9 h-9 relative"
				use:clickOutside={() => {
					showOptions = false;
				}}
			>
				{#if hovering && deletable}
					<IconButton
						size="button"
						style="padding: 0px"
						on:click={(e) => {
							e.stopPropagation();
							showOptions = !showOptions;
						}}
					>
						<Icon tag="svg" viewBox="0 0 24 24">
							<path fill="black" d={mdiDotsHorizontal} />
						</Icon>
					</IconButton>
				{/if}
				{#if showOptions}
					<div class="top-0 right-0 absolute mt-9 hover:bg-grey-lighter z-30">
						<Paper style="padding: 3px 0px;" elevation={7}>
							<Content>
								<button
									class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										ZenoService.deleteReport(report.id).then(() => invalidate('app:reports'));
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
									<span class="text-xs">Remove</span>
								</button>
							</Content>
						</Paper>
					</div>
				{/if}
			</div>
		</div>
	</div>
	<p class="mr-2 text-base truncate flex-shrink-0">{report.ownerName}</p>
	<p class="my-2 mr-2 text-sm w-full text-left overflow-y-auto flex-grow">
		{report.description}
	</p>
	<div class="flex items-center w-full mb-2 mt-3">
		{#await ZenoService.getReportStats(report.id)}
			<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
		{:then stats}
			<Tooltip
				content={`This report has ${shortenNumber(stats.numProjects, 1)} project${
					stats.numProjects !== 1 ? 's' : ''
				} linked to it.`}
				theme={'zeno-tooltip'}
				position="bottom"
			>
				<ProjectStat icon={mdiFileTree} text={stats.numProjects} />
			</Tooltip>
			<Tooltip
				content={`This report has ${shortenNumber(stats.numElements, 1)} element${
					stats.numElements !== 1 ? 's' : ''
				}.`}
				theme={'zeno-tooltip'}
				position="bottom"
			>
				<ProjectStat icon={mdiSitemap} text={stats.numElements} />
			</Tooltip>
		{/await}
	</div>
</button>
