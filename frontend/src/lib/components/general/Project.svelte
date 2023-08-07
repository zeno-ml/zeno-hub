<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ZenoService, type ProjectConfig } from '$lib/zenoapi';
	import { mdiDotsHorizontal } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';

	export let project: ProjectConfig;

	let showOptions = false;
	let hovering = false;
</script>

<button
	on:click={() => goto(`/project/${project.uuid}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="border-solid p-2 m-1 rounded-lg border-primary-dark border-2"
>
	<div class="flex justify-between items-center">
		<span class="mr-2">{project.name}</span>
		<div
			class="w-9 h-9 relative"
			use:clickOutside={() => {
				showOptions = false;
			}}
		>
			{#if hovering}
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
									ZenoService.deleteProject(project.uuid).then(() => invalidateAll());
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
</button>
