<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ZenoService, type Report } from '$lib/zenoapi';
	import { mdiDotsHorizontal } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';

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
	class="border-solid m-1 rounded-sm border-grey-light border shadow-sm flex flex-col py-2 px-5 hover:shadow-md"
>
	<div class="flex justify-between items-center w-full py-1">
		<div class={deletable ? 'mr-5' : ''}>
			<p class="text-black text-lg text-left">{report.name}</p>
			<p class="mr-2 text-base truncate text-left">{report.ownerName}</p>
		</div>
		{#if deletable}
			<div
				class="w-9 h-9 relative"
				use:clickOutside={() => {
					showOptions = false;
				}}
			>
				{#if hovering}
					<IconButton
						size="button"
						on:click={(e) => {
							e.stopPropagation();
							showOptions = !showOptions;
						}}
					>
						<Icon tag="svg" viewBox="0 0 24 24">
							<path fill="black" d={mdiDotsHorizontal} />
						</Icon>
					</IconButton>
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
										<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon
										>&nbsp;
										<span class="text-xs">Remove</span>
									</button>
								</Content>
							</Paper>
						</div>
					{/if}
				{/if}
			</div>
		{/if}
	</div>
</button>
