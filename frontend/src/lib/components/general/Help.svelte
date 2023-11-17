<script lang="ts">
	import { browser } from '$app/environment';
	import { clickOutside } from '$lib/util/clickOutside';
	import { mdiHelp } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { fade } from 'svelte/transition';

	export let docsLink = 'https://zenoml.com/docs/intro';
	export let optionsBelow = false;

	let showOptions = false;
</script>

<div
	class="relative z-20 flex flex-col items-end rounded-full border border-l border-primary-dark bg-white"
	transition:fade={{ delay: 1000, duration: 1000 }}
>
	<IconButton on:click={() => (showOptions = !showOptions)}>
		<Icon tag="svg" viewBox="0 0 24 24">
			<path class="fill-primary-dark" d={mdiHelp} />
		</Icon>
	</IconButton>
	{#if showOptions}
		<button
			class="absolute {optionsBelow ? 'top-14' : 'bottom-14'} z-50"
			transition:fade={{ duration: 100 }}
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
							if (browser) window.open('https://github.com/zeno-ml/zeno-hub/issues', '_blank');
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">bug_report</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Report an Issue</span>
					</button>
					<button
						class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
						on:keydown={() => ({})}
						on:click={(e) => {
							e.stopPropagation();
							if (browser) location.href = 'mailto:hello@zenoml.com';
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">mail</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Ask a Question</span>
					</button>
					<button
						class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
						on:keydown={() => ({})}
						on:click={(e) => {
							e.stopPropagation();
							if (browser) window.open(docsLink, '_blank');
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">article</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Explore the Docs</span>
					</button>
				</Content>
			</Paper>
		</button>
	{/if}
</div>
