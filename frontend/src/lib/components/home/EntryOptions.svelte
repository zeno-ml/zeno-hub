<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { page } from '$app/stores';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import CopyProjectPopup from '$lib/components/popups/CopyProjectPopup.svelte';
	import type { Project, Report, User, ZenoService } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';

	export let showOptions = false;
	export let project: Project | null = null;
	export let report: Report | null = null;
	export let user: User | null = null;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const exploreTab = $page.route.id === '/(app)/home';

	let showConfirmDelete = false;
	let showCopy = false;

	function deleteEntry() {
		if (project !== null) {
			zenoClient.deleteProject(project.uuid).then(() => invalidate('app:projects'));
		} else if (report !== null) {
			zenoClient.deleteReport(report.id).then(() => invalidate('app:reports'));
		}
		showConfirmDelete = false;
	}
</script>

{#if showCopy && user !== null && project !== null}
	<CopyProjectPopup config={project} on:close={() => (showCopy = false)} {user} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message={`Are you sure you want to delete this ${project ? 'project' : 'report'}?`}
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => deleteEntry()}
	/>
{/if}
<div class="absolute right-0 top-0 z-30 mt-9 hover:bg-grey-lighter">
	<Paper style="padding: 3px 0px;" elevation={7}>
		<Content>
			{#if project}
				<button
					class="py flex w-20 items-center px-2 hover:bg-grey-lighter"
					on:click={(e) => {
						e.stopPropagation();
						showOptions = false;
						showCopy = true;
					}}
				>
					<Icon style="font-size: 18px;" class="material-icons">content_copy</Icon>&nbsp;
					<span class="text-xs">Copy</span>
				</button>
			{/if}
			{#if !exploreTab && ((project && project.ownerName === user?.name) || (report && report.ownerName === user?.name))}
				<button
					class="py flex w-20 items-center px-2 hover:bg-grey-lighter"
					on:click={(e) => {
						e.stopPropagation();
						showOptions = false;
						showConfirmDelete = true;
					}}
				>
					<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
					<span class="text-xs">Remove</span>
				</button>
			{/if}
		</Content>
	</Paper>
</div>
