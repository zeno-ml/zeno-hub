<script lang="ts">
	import { viewMap } from '$lib/components/instance-views/views/viewMap';
	import {
		ZenoService,
		type InstancesElement,
		type InstancesOptions,
		type InstancesTableRequest,
		type ReportElement
	} from '$lib/zenoapi';
	import { mdiChevronLeft, mdiChevronRight } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { noop } from 'svelte/internal';

	export let element: ReportElement;

	let instancesElementSpec: InstancesElement | undefined;
	let instancesOptions: InstancesOptions | undefined;
	let table: Record<string, unknown>[] | undefined = [];
	let page = 0;

	try {
		instancesElementSpec = JSON.parse(element.data as string) as InstancesElement;
	} catch (e) {
		noop();
	}

	if (instancesElementSpec) {
		ZenoService.getInstancesOptions(instancesElementSpec).then((r) => (instancesOptions = r));
	}

	$: if (instancesElementSpec) {
		ZenoService.getInstancesTable({
			sliceId: instancesElementSpec.sliceId,
			model: instancesElementSpec.modelName,
			offset: page * 2,
			limit: 2
		} as InstancesTableRequest).then((r) => (table = JSON.parse(r)));
	}
</script>

{#if instancesOptions !== undefined && instancesElementSpec && table}
	<div class="w-full">
		<div class="flex justify-between mb-2">
			<h3 class="text-lg">
				Slice <span class="font-semibold">{instancesOptions.sliceName} </span>
				{#if instancesElementSpec.modelName}
					model
					<span class="font-semibold">{instancesElementSpec.modelName}</span>
				{/if}
			</h3>
			<p>{page * 2 + 1} - {page * 2 + 2} of {instancesOptions.sliceSize}</p>
		</div>
		<div class="flex items-stretch w-full justify-between">
			<button
				class="mr-2 hover:bg-yellowish-light {page === 0
					? 'bg-yellowish-light'
					: ''}  flex items-center"
				disabled={page === 0}
				on:click={() => page--}
			>
				<div class="w-6 h-6 align-middle">
					<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
						<path fill={page === 0 ? 'grey' : 'black'} d={mdiChevronLeft} />
					</Icon>
				</div>
			</button>
			<div class="overflow-x-scroll flex flex-wrap content-start w-full h-full">
				{#if viewMap[instancesOptions.view] !== undefined && instancesOptions.idColumn !== undefined}
					{#each table as inst (inst[instancesOptions.idColumn])}
						<div class="m-auto mt-0">
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
			<button
				class="hover:bg-yellowish-light flex items-center
				{page * 2 + 2 >= instancesOptions.sliceSize ? 'bg-yellowish-light' : ''}"
				disabled={page * 2 + 2 >= instancesOptions.sliceSize}
				on:click={() => page++}
			>
				<div class="w-6 h-6">
					<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiChevronRight} />
					</Icon>
				</div>
			</button>
		</div>
	</div>
{/if}
