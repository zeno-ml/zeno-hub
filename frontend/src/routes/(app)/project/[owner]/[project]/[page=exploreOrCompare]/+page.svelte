<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';

	export let data;
</script>

{#if !data.hasData}
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
	<MetadataPanel compare={data.compare} />
	<div class="mx-5 flex flex-col flex-grow w-1">
		<InstanceView compare={data.compare} />
	</div>
{/if}
