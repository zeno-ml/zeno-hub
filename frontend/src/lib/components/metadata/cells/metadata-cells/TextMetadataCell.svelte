<script lang="ts">
	import { projectConfig } from '$lib/stores';
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
	import SearchOption from './SearchOption.svelte';
	import MatchWholeWordIcon from './static/MatchWholeWordIcon.svelte';
	import RegexIcon from './static/RegexIcon.svelte';

	export let col: ZenoColumn;
	export let filterPredicates: FilterPredicate[];
	export let updatePredicates: (predicates: FilterPredicate[]) => void;

	let searchString = '';
	let isRegex = false;
	let regexValid = true;
	let caseMatch = false;
	let wholeWordMatch = false;
	let refresh = 0;
	let noResultsText = 'No results';
	let results: string[] = [];
	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};

	$: {
		regexValid = true;
		if (isRegex) {
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
			operation: Operation.LIKE,
			value: searchString,
			join: Join._
		});
		if (filterPredicates.length > 1) {
			filterPredicates[filterPredicates.length - 1].join = Join.OR;
		}
		updatePredicates(filterPredicates);

		searchString = '';
	}

	async function searchItems(input: string): Promise<string[]> {
		if (isRegex) {
			try {
				new RegExp(input);
				noResultsText = 'No results';
			} catch (e) {
				noResultsText = 'Invalid Regex!';
				results = [];
			}
		}

		try {
			if ($projectConfig) {
				results = await ZenoService.filterStringMetadata($projectConfig.uuid, {
					column: col,
					filterString: input,
					isRegex: isRegex,
					caseMatch: caseMatch,
					wholeWordMatch: wholeWordMatch
				});
				return results;
			}
		} catch (e) {
			results = [];
			return results;
		}
		return results;
	}

	function optionClick(e: MouseEvent) {
		if (e.currentTarget instanceof HTMLElement) {
			let id = e.currentTarget.id;
			if (id === 'caseMatch') {
				caseMatch = !caseMatch;
			} else if (id === 'wholeWordMatch') {
				wholeWordMatch = !wholeWordMatch;
			} else {
				if (isRegex) {
					isRegex = false;
					noResultsText = 'No results';
					regexValid = true;
				} else {
					isRegex = true;
				}
			}
		}
		refresh++;
	}
</script>

<div class="flex items-center ml-1">
	{#key refresh}
		<AutoComplete
			id="autoinput"
			bind:text={searchString}
			placeholder={'Search'}
			{noResultsText}
			hideArrow={true}
			searchFunction={searchItems}
			cleanUserText={false}
			ignoreAccents={false}
			localFiltering={false}
			delay={200}
		>
			<div slot="no-results" let:noResultsText>
				<span style:color={regexValid ? '' : 'red'}>{noResultsText}</span>
			</div>
		</AutoComplete>
	{/key}
	<div class="ml-2.5 flex items-center">
		<SearchOption
			id={'caseMatch'}
			highlighted={caseMatch}
			on:click={optionClick}
			tooltipContent={'Match Case'}>Aa</SearchOption
		>
		<SearchOption
			id={'wholeWordMatch'}
			highlighted={wholeWordMatch}
			on:click={optionClick}
			tooltipContent={'Match Whole Word'}
		>
			<svelte:component this={MatchWholeWordIcon} />
		</SearchOption>
		<SearchOption
			id={'typeSelection'}
			highlighted={isRegex}
			on:click={optionClick}
			tooltipContent={'Use Regular Expression'}
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

<div class="flex flex-wrap height-fit items-center py-1">
	{#each filterPredicates as pred}
		<div class="px-1 py-2.5 bg-primary-light mx-1 my rouded width-fit">
			<span>
				{pred.operation === Operation.LIKE ? '/' : ''}
				{pred.value}
				{pred.operation === Operation.LIKE ? '/' : ''}
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
