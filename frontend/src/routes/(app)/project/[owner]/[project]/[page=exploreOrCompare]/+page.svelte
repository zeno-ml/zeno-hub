<script lang="ts">
	import { goto } from '$app/navigation';
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
	import Button from '@smui/button';

	export let data;

	let width: number;
</script>

<svelte:window bind:innerWidth={width} />

{#if width < 600}
	<div class="text-lg p-10 m-10 rounded-md bg-primary text-white">
		Projects are currently not supported on mobile. Please open this project on a computer, or check
		out some of the Zeno Reports.
	</div>
	<div class="m-auto text-center">
		<Button variant="raised" on:click={() => goto('/reports')}>Explore Reports</Button>
	</div>
{:else}
	<MetadataPanel compare={data.compare} />
	<div class="mx-5 flex flex-col flex-grow w-1">
		<InstanceView compare={data.compare} />
	</div>
{/if}
