<script lang="ts">
	import { viewMap } from '$lib/components/instance-views/views/viewMap';
	import { ZenoService, type InstancesTableRequest, type ReportElement } from '$lib/zenoapi';

	export let element: ReportElement;

	let instancesElementSpec = JSON.parse(element.data);
	let table = [];

	ZenoService.getInstancesTable({
		sliceId: instancesElementSpec.sliceId,
		model: instancesElementSpec.modelName,
		offset: 0,
		limit: 10
	} as InstancesTableRequest).then((r) => (table = JSON.parse(r)));

	// Project settings we need
	// * view
	// * idColumn
	// * dataColumn
	// * labelColumn
	// * modelColumn
</script>

<div class="overflow-y-auto flex flex-wrap content-start w-full h-full">
	{#if viewMap[$project.view] !== undefined && idColumn !== undefined}
		{#each table as inst (inst[idColumn])}
			<div class="mr-2 mt-2">
				<svelte:component
					this={viewMap[$project.view]}
					options={{}}
					entry={inst}
					{dataColumn}
					modelColumn={modelColumn?.id}
					{labelColumn}
				/>
			</div>
		{/each}
	{/if}
</div>
