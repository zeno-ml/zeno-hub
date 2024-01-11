<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { project } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import type { Chart, ZenoService } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';

	export let showOptions: boolean;
	export let showDelete: boolean;
	export let chart: Chart;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<button
	class="absolute right-0 top-0 z-30 mt-9 hover:bg-grey-lighter"
	use:clickOutside={() => (showOptions = !showOptions)}
	on:click={(e) => e.stopPropagation()}
	on:keydown={(e) => {
		if (e.key === 'Escape') {
			showOptions = false;
		}
	}}
>
	<Paper style="padding: 7px 0px 7px 0px;" elevation={7}>
		<Content>
			<button
				class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
				on:keydown={() => ({})}
				on:click={(e) => {
					e.stopPropagation();
					showOptions = false;
					zenoClient
						.addChart($project.uuid, {
							id: 0,
							name: 'Copy of ' + chart.name,
							type: chart.type,
							projectUuid: $project.uuid,
							parameters: chart.parameters
						})
						.then(() => invalidate('app:charts'));
				}}
			>
				<Icon style="font-size: 20px;" class="material-icons">content_copy</Icon>&nbsp;
				<span class="text-sm">Make a copy</span>
			</button>
			<button
				class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
				on:keydown={() => ({})}
				on:click={(e) => {
					e.stopPropagation();
					showOptions = false;
					showDelete = true;
				}}
			>
				<Icon style="font-size: 20px;" class="material-icons">delete_outline</Icon>&nbsp;
				<span class="text-sm">Delete</span>
			</button>
		</Content>
	</Paper>
</button>
