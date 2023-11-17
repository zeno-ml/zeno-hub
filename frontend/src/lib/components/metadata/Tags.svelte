<script lang="ts">
	import { tags } from '$lib/stores';
	import { tooltip } from '$lib/util/tooltip';
	import { mdiInformationOutline } from '@mdi/js';
	import { Icon } from '@smui/icon-button';
	import TagCell from './cells/TagCell.svelte';
</script>

{#if $tags.length > 0}
	<div class="mt-4 flex items-center justify-between">
		<div class="flex items-center justify-between">
			<h4>Tags</h4>
			<div
				class="h-6 w-6 cursor-help fill-grey-darker"
				use:tooltip={{
					text: 'Tags are named sets of data instances'
				}}
			>
				<Icon tag="svg" viewBox="-6 -6 36 36">
					<path d={mdiInformationOutline} />
				</Icon>
			</div>
		</div>
	</div>
	<div class="mb-2">
		{#each [...$tags.values()] as t}
			<TagCell tag={t} />
		{/each}
	</div>
{/if}
