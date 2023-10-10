<script lang="ts">
	import { viewMap } from '$lib/components/instance-views/views/viewMap';
	import {
		ZenoService,
		type ReportElement,
		type SliceElementOptions,
		type SliceElementSpec,
		type SliceTableRequest
	} from '$lib/zenoapi';
	import { mdiChevronLeft, mdiChevronRight } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { noop } from 'svelte/internal';

	export let element: ReportElement;

	let sliceElementSpec: SliceElementSpec | undefined;
	let sliceElementOptions: SliceElementOptions | undefined;
	let table: Record<string, unknown>[] | undefined = [];
	let page = 0;

	try {
		sliceElementSpec = JSON.parse(element.data as string) as SliceElementSpec;
	} catch (e) {
		noop();
	}

	if (sliceElementSpec) {
		ZenoService.getSliceElementOptions(sliceElementSpec).then((r) => (sliceElementOptions = r));
	}

	$: if (sliceElementSpec) {
		ZenoService.getSliceTable({
			sliceId: sliceElementSpec.sliceId,
			model: sliceElementSpec.modelName,
			offset: page * 2,
			limit: 2
		} as SliceTableRequest).then((r) => (table = JSON.parse(r)));
	}
</script>

{#if sliceElementOptions !== undefined && sliceElementSpec && table}
	<div class="w-full">
		<div class="flex justify-between mb-2">
			<h3 class="text-lg">
				Slice <span class="font-semibold">{sliceElementOptions.sliceName} </span>
				{#if sliceElementSpec.modelName}
					model
					<span class="font-semibold">{sliceElementSpec.modelName}</span>
				{/if}
			</h3>
			<p>{page * 2 + 1} - {page * 2 + 2} of {sliceElementOptions.sliceSize}</p>
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
				{#if viewMap[sliceElementOptions.view] !== undefined && sliceElementOptions.idColumn !== undefined}
					{#each table as inst (inst[sliceElementOptions.idColumn])}
						<div class="m-auto mt-0">
							<svelte:component
								this={viewMap[sliceElementOptions.view]}
								options={{}}
								entry={inst}
								dataColumn={sliceElementOptions.dataColumn}
								modelColumn={sliceElementOptions.modelColumn}
								labelColumn={sliceElementOptions.labelColumn}
							/>
						</div>
					{/each}
				{/if}
			</div>
			<button
				class="hover:bg-yellowish-light flex items-center
				{page * 2 + 2 >= sliceElementOptions.sliceSize ? 'bg-yellowish-light' : ''}"
				disabled={page * 2 + 2 >= sliceElementOptions.sliceSize}
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
