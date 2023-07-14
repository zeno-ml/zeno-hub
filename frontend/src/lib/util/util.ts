import { slicesForComparison } from '../stores';
import { doesModelDependOnPredicates, setModelForFilterPredicateGroup } from '$lib/api/slice';

import { ZenoColumnType, type ZenoColumn, type Slice } from '$lib/zenoapi';

export function getProjectRouteFromURL(url: URL) {
	let projectURL = url.origin;
	const pathParts = url.pathname.split('/');
	const projectIndex = pathParts.indexOf('project');
	for (let i = 1; i < projectIndex + 2; i++) {
		projectURL = projectURL + '/' + pathParts[i];
	}
	return projectURL;
}

export function columnHash(col: ZenoColumn) {
	return (
		(col.columnType === ZenoColumnType.METADATA ? '' : col.columnType) +
		col.name +
		(col.model ? col.model : '')
	);
}

/** Calculate the metric range for coloring histograms */
export function getMetricRange(res: number[][]): [number, number] {
	const range: [number, number] = [Infinity, -Infinity];
	let allNull = true;
	res.forEach((arr) =>
		arr.forEach((n) => {
			if (n !== null) {
				allNull = false;
			}
			range[0] = Math.min(range[0], n);
			range[1] = Math.max(range[1], n);
		})
	);
	if (allNull) {
		return [Infinity, -Infinity];
	}
	return range;
}

// update model dependent slices in compare tab
export function updateModelDependentSlices(name: string, mod: string, slis: Slice[]) {
	slis.forEach((sli) => {
		const preds = sli.filterPredicates.predicates;
		if (doesModelDependOnPredicates(preds)) {
			slicesForComparison.update((ms) => {
				ms.set(sli.sliceName + ' (' + name + ')', <Slice>{
					id: sli.id,
					sliceName: sli.sliceName + ' (' + name + ')',
					folderId: sli.folderId,
					filterPredicates: setModelForFilterPredicateGroup(sli.filterPredicates, mod)
				});
				return ms;
			});
		}
	});
}
