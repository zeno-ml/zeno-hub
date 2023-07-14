<script lang="ts">
	import autoAnimate from '@formkit/auto-animate';
	import { mdiTrashCanOutline } from '@mdi/js';
	import Button from '@smui/button';
	import { Svg } from '@smui/common';
	import IconButton, { Icon } from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import { Join, type FilterPredicateGroup, Operation } from '$lib/zenoapi';
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
</script>

<div class="group">
	<div class="group-join">
		{#if index > 0}
			<Svelecte
				placeholder={''}
				style={'width: 80px'}
				value={predicateGroup.join}
				on:change={(e) => {
					predicateGroup.join = e.detail.label;
					predicateGroup = predicateGroup;
				}}
				valueField="label"
				labelField="label"
				options={['AND', 'OR']}
			/>
		{/if}
		{#if index > -1}
			<IconButton on:click={deletePredicate} style="min-width: 60px; color: var(--G2)">
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="currentColor" d={mdiTrashCanOutline} />
				</Icon>
			</IconButton>
		{/if}
	</div>
	<div class="{index === -1 ? 'no-bg' : 'bg'} main">
		<ul use:autoAnimate>
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
		<div id="buttons">
			<Button
				color="secondary"
				on:click={() => {
					predicateGroup.predicates.push({
						column: undefined,
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
								column: undefined,
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

<style>
	.group {
		display: flex;
	}
	.group-join {
		margin-top: 5px;
		margin-right: 10px;
	}
	.no-bg {
		background: none;
		padding-left: 0px;
		margin-bottom: 0px;
	}
	.bg {
		margin-bottom: 10px;
		padding-left: 10px;
		background: rgba(0, 0, 0, 0.025);
	}
	#buttons {
		margin-bottom: 10px;
	}
	.main {
		border-radius: 4px;
		margin-top: 5px;
	}
	ul {
		list-style-type: none;
		margin-right: 10px;
		margin-bottom: 0px;
		padding-left: 0px;
	}
</style>
