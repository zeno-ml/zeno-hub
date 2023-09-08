<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { featureFlags } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
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
	class="border-solid m-1 rounded-lg border-primary border-2 w-64 flex flex-col"
>
	<div class="flex justify-between items-center w-full px-2 py-1">
		<span class="mr-2 text-base truncate">{project.name}</span>
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
									ZenoService.deleteProject(project.uuid).then(() => invalidate('app:state'));
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
	{#if $featureFlags['PROJECT_STATS']}
		<div class="flex items-center w-full px-2 mb-2">
			{#await ZenoService.getProjectStats(project.uuid)}
				<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
			{:then stats}
				<ProjectStat icon={getProjectIcon()} text={stats.numInstances} />
				<ProjectStat icon={mdiLayersTriple} text={stats.numModels} />
				<ProjectStat icon={mdiChartBar} text={stats.numCharts} />
			{/await}
		</div>
	{/if}
</button>
