<script lang="ts">
	import { browser } from '$app/environment';
	import { clickOutside } from '$lib/util/clickOutside';
	import { tooltip } from '$lib/util/tooltip';
	import { mdiHelp } from '@mdi/js';
	import { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { fade } from 'svelte/transition';

	export let showOptions = false;

	let docsLink = 'https://zenoml.com/docs/intro';
</script>

<div class="relative mr-2">
	<button
		class="flex h-8 w-8 cursor-pointer items-center justify-center rounded-full border border-grey-light text-primary transition hover:bg-primary-mid"
		use:tooltip={{ text: 'Help' }}
		on:click={() => (showOptions = !showOptions)}
	>
		<Icon tag="svg" viewBox="0 0 24 24" class="w-5 fill-primary">
			<path d={mdiHelp} />
		</Icon>
	</button>

	{#if showOptions}
		<button
			class="absolute right-8 top-8 z-50"
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
