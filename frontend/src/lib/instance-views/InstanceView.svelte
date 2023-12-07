<script lang="ts">
	import Error from '$lib/instance-views/Error.svelte';
	import { elementMap, isComplexElement } from '$lib/instance-views/resolve.js';
	import type { ViewSchema } from '$lib/instance-views/schema';
	import schema from '$lib/instance-views/schema.json';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import Ajv from 'ajv';
	import { createEventDispatcher } from 'svelte';

	export let view: string;
	export let entry: Record<string, unknown>;
	export let idColumn: string | undefined | null;
	export let dataColumn: string | undefined | null;
	export let labelColumn: string | undefined | null;
	export let systemColumn: string | undefined | null;
	export let selectable = false;
	export let highlighted = false;

	const dispatch = createEventDispatcher();
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
		if (validate && !validate(viewSpec)) {
			schemaValidationError = ajv.errorsText(validate.errors, {
				dataVar: 'View Specification',
				separator: '\n'
			});
		} else {
			schemaValidationError = '';
		}
	} catch (error) {
		JSONParseError = error as string;
	}

	$: entryId = idColumn ? (entry[idColumn] as string) : null;
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
		{#if entryId}
			<div class="flex h-10 w-full items-center justify-between pl-4">
				<div class="text-xs text-grey-darker">
					{entryId}
				</div>
				{#if selectable && (hovering || highlighted)}
					<Checkbox checked={highlighted} on:click={() => dispatch('select')} />
				{/if}
			</div>
		{/if}
		<div class="px-4 pb-4 {!entryId ? 'pt-4' : ''}">
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
					<div class="mt-2 text-grey-darker">label</div>
					<div class="flex {isComplexElement(viewSpec.label.type) ? 'flex-col' : 'flex-row'}">
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
					<div class="mt-2 text-grey-darker">output</div>
					<div class="flex {isComplexElement(viewSpec.output.type) ? 'flex-col' : 'flex-row'}">
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
