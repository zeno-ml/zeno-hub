<script lang="ts">
	import { project } from '$lib/stores';
	import Button, { Label } from '@smui/button';
	import HomeButton from './HomeButton.svelte';

	export let isChartEdit: boolean | undefined;

	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};
</script>

<div class="ml-5 mt-5 flex cursor-pointer items-center">
	<HomeButton />
	{#if $project.editor}
		<Button
			class="ml-3"
			variant="raised"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => (isChartEdit = !isChartEdit)}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
	{/if}
</div>
