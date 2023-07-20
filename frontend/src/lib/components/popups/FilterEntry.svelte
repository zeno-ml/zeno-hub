<script lang="ts">
	import { mdiTrashCanOutline } from '@mdi/js';
	import { Svg } from '@smui/common';
	import IconButton, { Icon } from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import { model, columns } from '$lib/stores';
	import { MetadataType, ZenoColumnType, type FilterPredicate, Operation } from '$lib/zenoapi';
	import IdSearch from './IdSearch.svelte';

	export let predicate: FilterPredicate;
	export let deletePredicate: () => void;
	export let index: number;

	let operationMap = {
		'==': Operation.EQUAL,
		'!=': Operation.DIFFERENT,
		'>': Operation.GT,
		'<': Operation.LT,
		'>=': Operation.GTE,
		'<=': Operation.LTE
	};

	let inverseOperationMap = {
		[Operation.EQUAL]: '==',
		[Operation.DIFFERENT]: '!=',
		[Operation.GT]: '>',
		[Operation.LT]: '<',
		[Operation.GTE]: '>=',
		[Operation.LTE]: '<=',
		[Operation.LIKE]: 'LIKE'
	};
</script>

<div id="group">
	{#if index !== 0}
		<div class="selector">
			<Svelecte
				style={'width: 80px'}
				value={predicate.join}
				on:change={(e) => {
					// avoid backspace or delete
					predicate.join = e.detail !== null ? e.detail.label : 'AND';
				}}
				searchable={false}
				valueField="label"
				options={['AND', 'OR']}
			/>
		</div>
	{:else}
		<div style="width: 90px">
			<p>where</p>
		</div>
	{/if}
	<div class="selector">
		<Svelecte
			bind:value={predicate.column}
			placeholder={'Column'}
			valueAsObject
			valueField={'name'}
			options={$columns.filter(
				(d) =>
					d.columnType !== ZenoColumnType.EMBEDDING &&
					(d.model === $model ||
						d.columnType === ZenoColumnType.METADATA ||
						d.columnType === ZenoColumnType.PREDISTILL)
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
	<div class="selector">
		{#if predicate.column}
			{#if predicate.column.dataType === MetadataType.BOOLEAN}
				<Svelecte
					value={predicate.operation}
					on:change={(e) => {
						predicate.operation =
							e.detail !== null ? operationMap[e.detail.label] : Operation.EQUAL;
					}}
					valueField="label"
					placeholder={'Operation'}
					searchable={false}
					options={['==', '!=']}
				/>
			{:else if predicate.column.dataType === MetadataType.OTHER}
				<IdSearch col={$columns.filter((d) => d.name === 'id')[0]} bind:predicate />
			{:else}
				<Svelecte
					value={inverseOperationMap[predicate.operation]}
					on:change={(e) => {
						predicate.operation =
							e.detail !== null ? operationMap[e.detail.label] : Operation.EQUAL;
					}}
					valueField="label"
					placeholder={'Operation'}
					searchable={false}
					options={Object.keys(operationMap)}
				/>
			{/if}
		{/if}
	</div>

	<div>
		{#if predicate.column}
			{#if predicate.column.dataType === MetadataType.BOOLEAN}
				<Svelecte
					value={predicate.value + ''}
					on:change={(e) => {
						predicate.value = e.detail.label;
					}}
					valueField="label"
					placeholder={'Value'}
					searchable={false}
					options={['true', 'false']}
				/>
			{:else if predicate.column.dataType !== MetadataType.OTHER}
				<input type="text" bind:value={predicate.value} />
			{/if}
		{:else}
			<Svelecte />
		{/if}
	</div>
	<div class="selector">
		<IconButton on:click={deletePredicate} style="height:10px; margin-top: 5px; color: var(--G2)">
			<Icon component={Svg} viewBox="0 0 24 24">
				<path fill="currentColor" d={mdiTrashCanOutline} />
			</Icon>
		</IconButton>
	</div>
</div>

<style>
	.selector {
		margin-right: 10px;
	}
	#group {
		display: flex;
		flex-direction: inline;
		margin-bottom: 5px;
		margin-top: 5px;
	}
	input {
		height: 34px;
		border: 1px solid #ccc;
		border-radius: 4px;
	}
	p {
		margin: 0px;
		margin-left: 5px;
		margin-top: 5px;
	}
</style>
