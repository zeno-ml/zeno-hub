<script lang="ts">
	import Error from '$lib/instance-views/Error.svelte';
	import { elementMap, isComplexElement } from '$lib/instance-views/resolve.js';
	import type { ViewSchema } from '$lib/instance-views/schema';
	import schema from '$lib/instance-views/schema.json';
	import { columns, selectionIds } from '$lib/stores';
	import { ZenoColumnType } from '$lib/zenoapi';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import Ajv from 'ajv';

	export let view: string;
	export let entry: Record<string, unknown>;
	export let dataColumn: string | undefined | null;
	export let labelColumn: string | undefined | null;
	export let systemColumn: string | undefined | null;
	export let selectable = false;

	const ajv = new Ajv();
	ajv.addSchema(schema);
	const validate = ajv.getSchema('#/definitions/ViewSchema');

	let viewSpec: ViewSchema;
	let JSONParseError = '';
	let schemaValidationError = '';
	let hovering = false;

	$: try {
		viewSpec = JSON.parse(view);
		JSONParseError = '';
		if (validate) {
			if (!validate(viewSpec)) {
				schemaValidationError = ajv.errorsText(validate.errors, {
					dataVar: 'View Specification',
					separator: '\n'
				});
			} else {
				schemaValidationError = '';
			}
		}
	} catch (error) {
		JSONParseError = error as string;
	}

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID);
	$: entryId = idColumn ? (entry[idColumn.id] as string) : '';

	$: highlighted = selectable ? $selectionIds.includes(entryId) : false;
</script>

{#if JSONParseError}
	<Error type="Invalid JSON for View Specification" message={JSONParseError} />
{:else if schemaValidationError}
	<Error type="Invalid View Specification" message={schemaValidationError} />
{:else}
	<div
		class="cursor-default overflow-x-auto break-words rounded border border-grey-lighter {highlighted
			? 'border-primary'
			: ''}"
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
	>
		<div class="flex h-10 w-full items-center justify-between pl-4">
			<div class="text-xs text-grey-light">
				{entryId}
			</div>
			{#if selectable && (hovering || $selectionIds.includes(entryId))}
				<Checkbox
					checked={$selectionIds.includes(entryId)}
					on:click={() =>
						$selectionIds?.includes(entryId)
							? selectionIds.set($selectionIds.filter((id) => id !== entryId))
							: selectionIds.set([...$selectionIds, entryId])}
				/>
			{/if}
		</div>
		<div class="px-4 pb-4">
			{#if viewSpec.displayType === 'table'}
				<table class="overflow-x-auto break-words rounded border border-grey-lighter p-4">
					{#if dataColumn && entry[dataColumn] !== undefined && viewSpec.data}
						<svelte:component
							this={elementMap[viewSpec.data.type]}
							spec={viewSpec.data}
							data={typeof entry[dataColumn] === 'object'
								? JSON.stringify(entry[dataColumn])
								: entry[dataColumn]}
						/>
					{/if}
					{#if labelColumn && entry[labelColumn] !== undefined && viewSpec.label}
						<svelte:component
							this={elementMap[viewSpec.label.type]}
							spec={viewSpec.label}
							data={typeof entry[labelColumn] === 'object'
								? JSON.stringify(entry[labelColumn])
								: entry[labelColumn]}
						/>
					{/if}
					{#if systemColumn && entry[systemColumn] !== undefined && viewSpec.output}
						<svelte:component
							this={elementMap[viewSpec.output.type]}
							spec={viewSpec.output}
							data={typeof entry[systemColumn] === 'object'
								? JSON.stringify(entry[systemColumn])
								: entry[systemColumn]}
						/>
					{/if}
				</table>
			{:else}
				{#if dataColumn && entry[dataColumn] !== undefined && viewSpec.data}
					<div class="flex {isComplexElement(viewSpec.data.type) ? 'flex-col' : 'flex-row'}">
						<svelte:component
							this={elementMap[viewSpec.data.type]}
							spec={viewSpec.data}
							data={typeof entry[dataColumn] === 'object'
								? JSON.stringify(entry[dataColumn])
								: entry[dataColumn]}
						/>
					</div>
				{/if}
				{#if labelColumn && entry[labelColumn] !== undefined && viewSpec.label}
					<div class="flex {isComplexElement(viewSpec.label.type) ? 'flex-col' : 'flex-row'} mt-2">
						<span class="pr-2 font-semibold">label: </span>
						<svelte:component
							this={elementMap[viewSpec.label.type]}
							spec={viewSpec.label}
							data={typeof entry[labelColumn] === 'object'
								? JSON.stringify(entry[labelColumn])
								: entry[labelColumn]}
						/>
					</div>
				{/if}
				{#if systemColumn && entry[systemColumn] !== undefined && viewSpec.output}
					<hr class="-mx-4 my-4 text-grey-lighter" />
					<div class="flex {isComplexElement(viewSpec.output.type) ? 'flex-col' : 'flex-row'}">
						<span class="pr-2 font-semibold">output: </span>
						<svelte:component
							this={elementMap[viewSpec.output.type]}
							spec={viewSpec.output}
							data={typeof entry[systemColumn] === 'object'
								? JSON.stringify(entry[systemColumn])
								: entry[systemColumn]}
						/>
					</div>
				{/if}
			{/if}
		</div>
	</div>
{/if}
