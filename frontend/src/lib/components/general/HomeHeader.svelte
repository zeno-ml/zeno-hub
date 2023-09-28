<script lang="ts">
	import { page } from '$app/stores';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let user = '';

	let view = $page.route.id?.split('/').reverse()[0];
</script>

<div class="flex mb-4 h-8 ml-2">
	<Tooltip
		content={'Projects are datasets and system outputs for evaluation'}
		theme={'zeno-tooltip'}
		position="bottom"
	>
		<a
			href={user ? '/' + user + '/projects' : '/projects'}
			class="text-xl mr-6 text-black hover:text-primary
        {view === 'projects' ? 'border-b-2 border-primary' : ''}"
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
        {view === 'reports' ? 'border-b-2 border-primary' : ''}"
		>
			Reports
		</a>
	</Tooltip>
</div>
