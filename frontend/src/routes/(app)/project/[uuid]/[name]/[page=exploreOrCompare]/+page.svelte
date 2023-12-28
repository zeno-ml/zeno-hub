<script lang="ts">
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/general/Banner.svelte';
	import Instances from '$lib/components/instances/Instances.svelte';
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
	import Button from '@smui/button';

	export let data;

	let width: number;
</script>

<svelte:window bind:innerWidth={width} />

{#if width < 600}
	<div class="m-10 rounded-md bg-primary-dark p-10 text-lg text-white">
		Projects are currently not supported on mobile. Please open this project on a computer, or check
		out some of the Zeno Reports.
	</div>
	<div class="m-auto text-center">
		<Button variant="raised" on:click={() => goto('/reports')}>Explore Reports</Button>
	</div>
{:else if !data.hasData}
	<div class="m-auto text-center">
		<Banner>
			Your haven't uploaded any data to your project yet.
			<br />
			Follow the
			<a class="text-primary hover:underline" href="https://zenoml.com/docs/intro"
				>Getting Started Guide</a
			> to learn how to upload a dataset and AI system outputs.
		</Banner>
	</div>
{:else}
	<div class="flex h-full min-h-0 w-full min-w-0">
		<MetadataPanel compare={data.compare} />
		<div class="flex w-full min-w-0 flex-col px-3">
			<Instances compare={data.compare} />
		</div>
	</div>
{/if}
