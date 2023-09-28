<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { clickOutside } from '$lib/util/clickOutside';
	import { shortenNumber } from '$lib/util/util';
	import { ZenoService, type Project } from '$lib/zenoapi';
	import {
		mdiChartBar,
		mdiDotsHorizontal,
		mdiImage,
		mdiLayersTriple,
		mdiTag,
		mdiText
	} from '@mdi/js';
	import { Icon } from '@smui/button';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import ProjectStat from './ProjectStat.svelte';

	export let project: Project;
	export let deletable = false;

	let showOptions = false;
	let hovering = false;

	function getProjectIcon() {
		if (project.view.includes('image')) return mdiImage;
		if (project.view.includes('chat') || project.view.includes('text')) return mdiText;
		else return mdiTag;
	}
</script>

<button
	on:click={() => goto(`/project/${project.ownerName}/${project.name}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="border-solid m-1 rounded-lg border-grey-light border shadow-sm flex flex-col p-3 px-5 hover:shadow-md w-80 h-60"
>
	<div class="flex flex-col w-full">
		<div class="flex justify-between items-center">
			<p class="mr-2 truncate text-black text-lg">{project.name}</p>
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
										ZenoService.deleteProject(project.uuid).then(() => invalidate('app:projects'));
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
	<p class="mr-2 text-base truncate flex-shrink-0">{project.ownerName}</p>
	<p class="my-2 mr-2 text-sm w-full text-left overflow-y-auto flex-grow">
		{project.description}
	</p>
	<div class="flex items-center w-full mb-2 mt-3">
		{#await ZenoService.getProjectStats(project.uuid)}
			<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
		{:then stats}
			<Tooltip
				content={`This project has ${shortenNumber(stats.numInstances, 1)} data point${
					stats.numInstances !== 1 ? 's' : ''
				}.`}
				theme={'zeno-tooltip'}
				position="bottom"
			>
				<ProjectStat icon={getProjectIcon()} text={stats.numInstances} />
			</Tooltip>
			<Tooltip
				content={`This project has ${shortenNumber(stats.numModels, 1)} system${
					stats.numModels !== 1 ? 's' : ''
				}.`}
				theme={'zeno-tooltip'}
				position="bottom"
			>
				<ProjectStat icon={mdiLayersTriple} text={stats.numModels} />
			</Tooltip>
			<Tooltip
				content={`This project has ${shortenNumber(stats.numCharts, 1)} chart${
					stats.numCharts !== 1 ? 's' : ''
				}.`}
				theme={'zeno-tooltip'}
				position="bottom"
			>
				<ProjectStat icon={mdiChartBar} text={stats.numCharts} />
			</Tooltip>
		{/await}
	</div>
</button>
