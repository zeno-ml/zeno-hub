<script lang="ts">
	import { page } from '$app/stores';
	import { showNewReport } from '$lib/stores';
	import { tooltip } from '$lib/util/tooltip';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';

	export let user = '';

	let view = $page.route.id?.split('/').reverse()[0];
</script>

<div class="flex mb-4 items-center h-10">
	<a
		href={user ? '/' + user + '/projects' : '/projects'}
		class="text-xl mr-6 text-black hover:text-primary p-2 rounded
        {view === 'projects' ? 'bg-grey-lighter' : 'text-grey-dark'}"
		use:tooltip={{ text: 'Projects are collections of datasets, models, and evaluations' }}
	>
		Projects
	</a>
	<a
		href={user ? '/' + user + '/reports' : '/reports'}
		class="text-xl mr-6 text-black hover:text-primary p-2 rounded
        {view === 'reports' ? 'bg-grey-lighter' : 'text-grey-dark'}"
		use:tooltip={{ text: 'Reports are interactive notebooks for sharing evaluation insights' }}
	>
		Reports
	</a>
	{#if view === 'reports' && user}
		<Button on:click={() => showNewReport.set(true)}>
			<Icon class="material-icons" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
				<path d={mdiPlus} />
			</Icon>
			New Report
		</Button>
	{/if}
</div>
{#if view === 'projects' && !user}
	<p class="italic text-lg mb-4 ml-1 text-grey-dark">
		Explore, evaluate, and visualize AI systems with Zeno Projects. <a
			class="text-primary"
			href="http://zenoml.com">Learn more!</a
		>
	</p>
{:else if view === 'reports' && !user}
	<p class="italic text-lg mb-4 ml-1 text-grey-dark">
		Author interactive, data-driven AI evaluation reports.
		<a class="text-primary" href="http://zenoml.com">Learn more!</a>
	</p>
{/if}
