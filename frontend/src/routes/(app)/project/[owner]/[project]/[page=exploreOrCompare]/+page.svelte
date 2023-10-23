<script lang="ts">
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/general/Banner.svelte';
	import Instances from '$lib/components/instances/Instances.svelte';
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
	import ProjectHeader from '$lib/components/project/ProjectHeader.svelte';
	import Button from '@smui/button';

	export let data;

	let likes = data.numLikes;
	let liked = data.userLiked;
	let width: number;
</script>

<svelte:window bind:innerWidth={width} />

{#if width < 600}
	<div class="text-lg p-10 m-10 rounded-md bg-primary-dark text-white">
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
	<div class="flex flex-col w-full h-full min-h-0">
		<ProjectHeader project={data.project} bind:likes bind:liked user={data.user} />
		<div class="flex h-full min-h-0">
			<MetadataPanel compare={data.compare} />
			<div class="mx-5 flex flex-col flex-grow w-1">
				<Instances compare={data.compare} />
			</div>
		</div>
	</div>
{/if}
