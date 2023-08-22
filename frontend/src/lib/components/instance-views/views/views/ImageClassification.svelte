<script lang="ts">
	import { authToken } from '$lib/stores';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: fetchImage = (async () => {
		const response = await fetch(entry['data'] as string, {
			headers: {
				Authorization: 'Bearer ' + $authToken
			}
		});
		return await response.blob();
	})();
</script>

{#await fetchImage}
	<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
{:then data}
	<div class="w-min p-2 border border-grey-lighter" style:background-color="white">
		<img
			src={URL.createObjectURL(data)}
			style:max-width="200px"
			alt="Image thumbnail for instance {entry['data_id']}"
		/>
		<br />
		<div class="flex">
			<span class="mr-2 text-xs">label: </span>
			<span class="value text-xs">{entry['label']}</span>
		</div>
		{#if modelColumn && entry[modelColumn]}
			<div class="flex">
				<span class="mr-2 text-xs">output: </span>
				<span class="value text-xs">{entry[modelColumn]} </span>
			</div>
		{/if}
	</div>
{/await}
