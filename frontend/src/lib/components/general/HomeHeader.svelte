<script lang="ts">
	import { page } from '$app/stores';
	import { showNewReport } from '$lib/stores';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let user = '';

	let view = $page.route.id?.split('/').reverse()[0];
</script>

<div class="flex ml-2 items-center h-8">
	<Tooltip
		content={'Projects are datasets and system outputs for evaluation'}
		theme={'zeno-tooltip'}
		position="bottom"
	>
		<a
			href={user ? '/' + user + '/projects' : '/projects'}
			class="text-xl mr-6 text-black hover:text-primary
        {view === 'projects' ? '' : 'text-grey-dark'}"
		>
			Projects
		</a>
	</Tooltip>
	<Tooltip
		content={'Reports are interactive notebooks for sharing evaluation insights'}
		theme={'zeno-tooltip'}
		position="bottom"
	>
		<a
			href={user ? '/' + user + '/reports' : '/reports'}
			class="text-xl mr-4 hover:text-primary
        {view === 'reports' ? '' : 'text-grey-dark'}"
		>
			Reports
		</a>
	</Tooltip>
	{#if view === 'reports' && user}
		<Button class="ml-auto" on:click={() => showNewReport.set(true)}>
			<Icon class="material-icons" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
				<path d={mdiPlus} />
			</Icon>
			New Report
		</Button>
	{/if}
</div>
<div class="w-full mb-4 h-1 bg-grey-light rounded-full" />
