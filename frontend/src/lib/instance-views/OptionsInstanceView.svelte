<script lang="ts">
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import { columns, selectionIds } from '$lib/stores';
	import { ZenoColumnType } from '$lib/zenoapi';
	import Checkbox from '@smui/checkbox';

	export let view: string;
	export let dataColumn: string | undefined;
	export let labelColumn: string | undefined;
	export let modelColumn: string | undefined;
	export let entry: Record<string, string | number | boolean>;

	let hovering = false;

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID);
	$: entryId = idColumn ? (entry[idColumn.id] as string) : '';
</script>

<div
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => {
		hovering = false;
	}}
	on:blur={() => {
		hovering = false;
	}}
	tabindex="0"
	role="button"
	class="relative"
>
	{#if hovering || $selectionIds.includes(entryId)}
		<div class="absolute right-0 top-0 z-10">
			<Checkbox
				checked={$selectionIds.includes(entryId)}
				on:click={() =>
					$selectionIds?.includes(entryId)
						? selectionIds.set($selectionIds.filter((id) => id !== entryId))
						: selectionIds.set([...$selectionIds, entryId])}
			/>
		</div>
	{/if}
	<InstanceView
		{view}
		{dataColumn}
		{labelColumn}
		{modelColumn}
		{entry}
		highlighted={$selectionIds.includes(entryId)}
	/>
</div>
