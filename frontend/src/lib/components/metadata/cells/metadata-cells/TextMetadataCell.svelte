<script lang="ts">
	import { project } from '$lib/stores';
	import {
		Join,
		Operation,
		ZenoService,
		type FilterPredicate,
		type ZenoColumn
	} from '$lib/zenoapi';
	import Button from '@smui/button';
	import { TrailingIcon } from '@smui/chips';
	import { Label } from '@smui/common';
	import AutoComplete from 'simple-svelte-autocomplete';
	import { getContext } from 'svelte';
	import SearchOption from './SearchOption.svelte';
	import RegexIcon from './static/RegexIcon.svelte';

	export let col: ZenoColumn;
	export let filterPredicates: FilterPredicate[];
	export let updatePredicates: (predicates: FilterPredicate[]) => void;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let operation = Operation.ILIKE;
	let searchString = '';
	let regexValid = true;
	let noResultsText = 'No results';
	let results: string[] = [];
	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};

	$: {
		regexValid = true;
		if (operation === Operation.REGEX) {
			try {
				new RegExp(searchString);
			} catch (e) {
				regexValid = false;
			}
		}
	}

	function setSelection() {
		if (!searchString) {
			return;
		}

		filterPredicates.push({
			column: col,
			operation: operation,
			value: searchString,
			join: Join._
		});

		if (filterPredicates.length > 1) {
			filterPredicates[filterPredicates.length - 1].join = Join.OR;
		}

		updatePredicates(filterPredicates);

		searchString = '';
	}

	async function searchData(input: string): Promise<string[]> {
		if (operation === Operation.REGEX) {
			try {
				new RegExp(input);
				noResultsText = 'No results';
			} catch (e) {
				noResultsText = 'Invalid Regex!';
				results = [];
			}
		}

		try {
			results = await zenoClient.filterStringMetadata($project.uuid, {
				column: col,
				filterString: input,
				operation: operation
			});
		} catch (e) {
			results = [];
		}
		return results;
	}
</script>

<div class="ml-1 flex items-center">
	<AutoComplete
		id="autoinput"
		bind:text={searchString}
		placeholder={'Search'}
		{noResultsText}
		hideArrow={true}
		searchFunction={searchData}
		cleanUserText={false}
		ignoreAccents={false}
		localFiltering={false}
		delay={200}
	>
		<div slot="no-results" let:noResultsText>
			<span style:color={regexValid ? '' : 'red'}>{noResultsText}</span>
		</div>
	</AutoComplete>
	<div class="ml-2.5 flex items-center rounded-md border border-grey-light">
		<SearchOption
			id={'caseMatch'}
			highlighted={operation === Operation.LIKE}
			on:click={() =>
				operation === Operation.LIKE ? (operation = Operation.ILIKE) : (operation = Operation.LIKE)}
			tooltipContent={'Match Case'}>Aa</SearchOption
		>
		<div class="h-6 w-px bg-grey-light" />
		<SearchOption
			id={'typeSelection'}
			highlighted={operation === Operation.REGEX}
			on:click={() =>
				operation === Operation.REGEX
					? (operation = Operation.ILIKE)
					: (operation = Operation.REGEX)}
			tooltipContent={'Use POSIX Regular Expression'}
		>
			<svelte:component this={RegexIcon} />
		</SearchOption>
	</div>
	<Button
		style="margin-left: 10px; height: 32px"
		variant="outlined"
		on:click={setSelection}
		on:mouseleave={blur}
		on:focusout={blur}
	>
		<Label>Set</Label>
	</Button>
</div>

<div class="height-fit flex flex-wrap items-center py-1">
	{#each filterPredicates as pred}
		<div class="my rouded width-fit mx-1 bg-primary-light px-1 py-2.5">
			<span>
				{pred.value}
			</span>
			<TrailingIcon
				class="remove material-icons"
				on:click={() => {
					filterPredicates = filterPredicates.filter((p) => p !== pred);
					if (filterPredicates.length > 0) {
						filterPredicates[0].join = Join._;
					}
					updatePredicates(filterPredicates);
				}}
			>
				cancel
			</TrailingIcon>
		</div>
	{/each}
</div>
