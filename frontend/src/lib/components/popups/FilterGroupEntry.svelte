<script lang="ts">
	import { columns } from '$lib/stores';
	import { Join, Operation, type FilterPredicateGroup } from '$lib/zenoapi';
	import autoAnimate from '@formkit/auto-animate';
	import { mdiTrashCanOutline } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import FilterEntry from './FilterEntry.svelte';

	export let predicateGroup: FilterPredicateGroup;
	export let deletePredicate: () => void;
	export let index: number;

	function deletePredicateLocal(localIndex: number) {
		predicateGroup.predicates.splice(localIndex, 1);
		if (predicateGroup.predicates.length === 0) {
			deletePredicate();
			return;
		} else {
			predicateGroup.predicates[0].join = Join._;
		}
		predicateGroup = predicateGroup;
	}

	function joinChange(e: CustomEvent) {
		predicateGroup.join = e.detail.label;
		predicateGroup = predicateGroup;
	}
</script>

<div class="flex">
	<div class="mr-2.5 mt-1">
		{#if index > 0}
			<Svelecte
				placeholder={''}
				style={'width: 80px'}
				value={predicateGroup.join}
				on:change={joinChange}
				valueField="label"
				labelField="label"
				options={['AND', 'OR']}
			/>
		{/if}
		{#if index > -1}
			<IconButton on:click={deletePredicate} class="min-w-[60px] text-grey-dark">
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="currentColor" d={mdiTrashCanOutline} />
				</Icon>
			</IconButton>
		{/if}
	</div>
	<div class="{index === -1 ? '' : 'border border-primary-mid p-2'} mt-1 rounded">
		<ul use:autoAnimate class="mr-2.5 list-none">
			{#each predicateGroup.predicates as p, i}
				{#if !('predicates' in p)}
					<li>
						<FilterEntry
							index={i}
							deletePredicate={() => deletePredicateLocal(i)}
							bind:predicate={p}
						/>
					</li>
				{:else}
					<svelte:self
						index={i + 1 + index}
						deletePredicate={() => deletePredicateLocal(i)}
						bind:predicateGroup={p}
					/>
				{/if}
			{/each}
		</ul>
		<div class="mb-2.5 mt-4">
			<Button
				color="secondary"
				on:click={() => {
					predicateGroup.predicates.push({
						column: $columns[0],
						operation: Operation.EQUAL,
						value: '',
						join: predicateGroup.predicates.length === 0 ? Join._ : Join.AND
					});
					predicateGroup = predicateGroup;
				}}
			>
				add filter
			</Button>
			<Button
				color="secondary"
				on:click={() => {
					predicateGroup.predicates.push({
						predicates: [
							{
								column: $columns[0],
								operation: Operation.EQUAL,
								value: '',
								join: Join._
							}
						],
						join: predicateGroup.predicates.length === 0 ? Join._ : Join.AND
					});
					predicateGroup = predicateGroup;
				}}
			>
				add group
			</Button>
		</div>
	</div>
</div>
