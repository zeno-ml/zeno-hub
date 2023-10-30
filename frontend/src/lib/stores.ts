import {
	Join,
	type Chart,
	type FilterPredicate,
	type FilterPredicateGroup,
	type Folder,
	type Metric,
	type Project,
	type Slice,
	type Tag,
	type ZenoColumn
} from '$lib/zenoapi';
import { interpolate } from 'd3-interpolate';
import { derived, get, writable, type Readable, type Writable } from 'svelte/store';

export const project: Writable<Project> = writable();
export const slices: Writable<Slice[]> = writable([]);
export const columns: Writable<ZenoColumn[]> = writable([]);
export const models: Writable<string[]> = writable([]);
export const model: Writable<string | undefined> = writable(undefined);
export const comparisonModel: Writable<string | undefined> = writable(undefined);
export const comparisonColumn: Writable<ZenoColumn | undefined> = writable(undefined);
export const metrics: Writable<Metric[]> = writable([]);
export const metric: Writable<Metric | undefined> = writable(undefined);
export const rowsPerPage: Writable<number> = writable(5);
export const folders: Writable<Folder[]> = writable([]);
export const tags: Writable<Tag[]> = writable([]);
export const charts: Writable<Chart[]> = writable([]);
export const collapseHeader: Writable<boolean> = writable(false);

// [column, ascending]
export const sort: Writable<[ZenoColumn | undefined, boolean]> = writable([undefined, true]);

export const requestingHistogramCounts: Writable<boolean> = writable(false);

// Slices dependent on models will be separate into two new slices in the comparison tab
// and stored in this writable for model output comparison
export const slicesForComparison: Writable<Slice[]> = writable([]);
export const compareSort: Writable<[ZenoColumn | undefined, boolean]> = writable([undefined, true]);

// The tag ids selected by the user.
export const tagIds: Writable<string[] | undefined> = writable(undefined);
export const editTag: Writable<Tag | undefined> = writable(undefined);
export const editedIds: Writable<string[]> = writable([]);

// The ids directly selected by the user.
export const selectionIds: Writable<string[] | undefined> = writable(undefined);
export const selections: Writable<{
	metadata: Record<string, FilterPredicateGroup>;
	slices: number[];
	tags: number[];
}> = writable({
	metadata: {},
	slices: [],
	tags: []
});
// Combination of selected filters and slice filters.
// Needs to be a group because we need to join the predicates with &.
export const selectionPredicates: Readable<FilterPredicateGroup | undefined> = derived(
	[selections],
	([$selections]) => {
		const predicateGroup: FilterPredicateGroup = { predicates: [], join: Join._ };
		// Pre-fill slice creation with current metadata selections.
		// Join with AND.
		predicateGroup.predicates = Object.values($selections.metadata)
			.filter((d) => d.predicates.length > 0)
			.flat()
			.map((d, i) => {
				d.join = i === 0 && $selections.slices.length === 0 ? Join._ : Join.AND;
				return d;
			});

		// if slices are not empty in $selections, add slice filters
		if ($selections.slices.length > 0) {
			let slicesPredicates: (FilterPredicate | FilterPredicateGroup)[] = [];
			$selections.slices.map((s, i) => {
				const sli =
					get(slices).findIndex((sls) => sls.id === s) !== -1
						? get(slices).find((slice) => slice.id === s)
						: get(slicesForComparison).find((slice) => slice.id === s);
				const sli_preds = JSON.parse(
					JSON.stringify(sli !== undefined ? sli.filterPredicates.predicates : undefined)
				);
				sli_preds[0].join = i === 0 ? Join._ : Join.AND;
				slicesPredicates = slicesPredicates.concat(sli_preds);
			});
			predicateGroup.predicates = [...slicesPredicates, ...predicateGroup.predicates];
		}
		return predicateGroup.predicates.length === 0 ? undefined : predicateGroup;
	}
);

export const metricRange: Writable<[number, number]> = writable([Infinity, -Infinity]);
export const metricRangeColorScale: Readable<(n: number) => string> = derived(
	[metricRange],
	([$metricRange]) => {
		const [min, max] = $metricRange;
		const colorScale = interpolate('#decbe9', '#6a1b9a');
		return (n: number) => {
			if (max === Infinity || min === Infinity) return colorScale(1);
			if (max - min === 0) return colorScale(0.5);
			if (n < min) return colorScale(0);
			if (n > max) return colorScale(1);
			return colorScale((n - min) / (max - min));
		};
	}
);

// Store the current state of feature flags
export const featureFlags: Writable<Record<string, boolean>> = writable({});

// Whether the new report popup should be displayed on the reports page
export const showNewReport = writable(false);

export interface TooltipSpec {
	hover: boolean;
	mousePos: { x: number; y: number };
	text: undefined | string;
}

export const tooltipState = writable<TooltipSpec>({
	hover: false,
	mousePos: { x: 0, y: 0 },
	text: undefined
});
