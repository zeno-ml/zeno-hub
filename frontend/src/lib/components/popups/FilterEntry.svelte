<script lang="ts">
	import { columns, model } from '$lib/stores';
	import { getOperation, inverseOperationMap } from '$lib/util/util';
	import {
		Join,
		MetadataType,
		Operation,
		ZenoColumnType,
		type FilterPredicate
	} from '$lib/zenoapi';
	import { mdiTrashCanOutline } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import Svelecte from 'svelecte';

	export let predicate: FilterPredicate;
	export let deletePredicate: () => void;
	export let index: number;

	function joinChange(e: CustomEvent) {
		// avoid backspace or delete
		predicate.join = e.detail !== null ? e.detail.label : Join.AND;
	}

	function operationChange(e: CustomEvent) {
		predicate.operation = e.detail !== null ? getOperation(e.detail.label) : Operation.EQUAL;
	}

	function predicateChange(e: CustomEvent) {
		predicate.value = e.detail.label;
	}
</script>

<div class="flex mb-1 mt-1">
	{#if index !== 0}
		<div class="mr-2.5">
			<Svelecte
				style={'width: 80px'}
				value={predicate.join}
				on:change={joinChange}
				searchable={false}
				valueField="label"
				options={['AND', 'OR']}
			/>
		</div>
	{:else}
		<div style="width: 90px">
			<p class="ml-1 mt-1">where</p>
		</div>
	{/if}
	<div class="mr-2.5">
		<Svelecte
			bind:value={predicate.column}
			placeholder={'Column'}
			valueAsObject
			valueField={'name'}
			options={$columns.filter(
				(d) =>
					d.columnType !== ZenoColumnType.EMBEDDING &&
					(d.model === $model || d.columnType === ZenoColumnType.FEATURE)
			)}
			on:change={() => {
				if (predicate.column.dataType === MetadataType.OTHER) {
					predicate.operation = Operation.LIKE;
				} else {
					predicate.operation = Operation.EQUAL;
				}
			}}
		/>
	</div>
	<div class="mr-2.5">
		{#if predicate.column}
			{#if predicate.column.dataType === MetadataType.BOOLEAN}
				<Svelecte
					value={predicate.operation}
					on:change={operationChange}
					valueField="label"
					placeholder={'Operation'}
					searchable={false}
					options={['==', '!=']}
				/>
			{:else}
				<Svelecte
					value={inverseOperationMap[predicate.operation]}
					on:change={operationChange}
					valueField="label"
					placeholder={'Operation'}
					searchable={false}
					options={['==', '!=', '>', '<', '>=', '<=', 'LIKE']}
				/>
			{/if}
		{/if}
	</div>

	<div>
		{#if predicate.column}
			{#if predicate.column.dataType === MetadataType.BOOLEAN}
				<Svelecte
					value={predicate.value + ''}
					on:change={predicateChange}
					valueField="label"
					placeholder={'Value'}
					searchable={false}
					options={['true', 'false']}
				/>
			{:else if predicate.column.dataType !== MetadataType.OTHER}
				<input
					type="text"
					bind:value={predicate.value}
					class="h-8 border border-grey-lighter rounded"
				/>
			{/if}
		{:else}
			<Svelecte />
		{/if}
	</div>
	<div class="mr-2.5">
		<IconButton on:click={deletePredicate} style="height:10px; margin-top: 5px; color: var(--G2)">
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="currentColor" d={mdiTrashCanOutline} />
			</Icon>
		</IconButton>
	</div>
</div>
