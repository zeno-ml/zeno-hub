<script lang="ts">
	import { viewMap } from '$lib/components/instance-views/views/viewMap';
	import {
		ZenoService,
		type InstancesElement,
		type InstancesOptions,
		type InstancesTableRequest,
		type ReportElement
	} from '$lib/zenoapi';

	export let element: ReportElement;

	let instancesElementSpec = JSON.parse(element.data) as InstancesElement;
	let instancesOptions: InstancesOptions | undefined;
	let table = [];

	ZenoService.getInstancesOptions(instancesElementSpec).then((r) => (instancesOptions = r));

	ZenoService.getInstancesTable({
		sliceId: instancesElementSpec.sliceId,
		model: instancesElementSpec.modelName,
		offset: 0,
		limit: 2
	} as InstancesTableRequest).then((r) => (table = JSON.parse(r)));
</script>

<h3 class="text-lg">
	Slice <span class="font-semibold">{instancesElementSpec.sliceId}</span> model
	<span class="font-semibold">{instancesElementSpec.modelName}</span>
</h3>
{#if instancesOptions && table.length > 0}
	<div class="overflow-y-auto flex flex-wrap content-start w-full h-full">
		{#if viewMap[instancesOptions.view] !== undefined && instancesOptions.idColumn !== undefined}
			{#each table as inst (inst[instancesOptions.idColumn])}
				<div class="mr-2 mt-2">
					<svelte:component
						this={viewMap[instancesOptions.view]}
						options={{}}
						entry={inst}
						dataColumn={instancesOptions.dataColumn}
						modelColumn={instancesOptions.modelColumn}
						labelColumn={instancesOptions.labelColumn}
					/>
				</div>
			{/each}
		{/if}
	</div>
{/if}
