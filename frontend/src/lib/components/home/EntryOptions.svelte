<script lang="ts">
	import { page } from '$app/stores';
	import type { Project, Report, User } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Paper, { Content } from '@smui/paper';

	export let showOptions = false;
	export let showConfirmDelete = false;
	export let showCopy = false;
	export let project: Project | null = null;
	export let report: Report | null = null;
	export let user: User | null = null;

	const exploreTab = $page.route.id === '/(app)/home';
</script>

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
