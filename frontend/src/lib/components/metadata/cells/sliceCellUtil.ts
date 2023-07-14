import { selections } from '$lib/stores';
import type { Slice } from '$lib/zenoapi';
import { get } from 'svelte/store';

/** click/unclick to select/deselect the slice
and with pressing shift key to select multiple slices */
export function selectSliceCell(e: MouseEvent, slice: Slice) {
	if (
		get(selections).slices.length === 1 &&
		get(selections).slices.some((currentSlice) => currentSlice === slice.id)
	) {
		selections.update((s) => ({
			slices: [],
			metadata: s.metadata,
			tags: s.tags
		}));
		return;
	}
	if (e.shiftKey) {
		if (get(selections).slices.some((currentSlice) => currentSlice === slice.id)) {
			selections.update((sel) => {
				sel.slices.splice(
					sel.slices.findIndex((currentSlice) => currentSlice === slice.id),
					1
				);
				return {
					slices: [...sel.slices],
					metadata: sel.metadata,
					tags: sel.tags
				};
			});
		} else {
			selections.update((sel) => ({
				slices: [...sel.slices, slice.id],
				metadata: sel.metadata,
				tags: sel.tags
			}));
		}
	} else {
		selections.update((sel) => ({
			slices: [slice.id],
			metadata: sel.metadata,
			tags: sel.tags
		}));
	}
}

/** click/unclick to select/deselect the slice for model depended slices */
export function selectModelDependSliceCell(slice: Slice) {
	if (get(selections).slices.some((currentSlice) => currentSlice === slice.id)) {
		selections.update((sel) => {
			sel.slices.splice(
				sel.slices.findIndex((currentSlice) => currentSlice === slice.id),
				1
			);
			return {
				slices: [...sel.slices],
				metadata: sel.metadata,
				tags: sel.tags
			};
		});
	} else {
		selections.update((sel) => ({
			slices: [...sel.slices, slice.id],
			metadata: sel.metadata,
			tags: sel.tags
		}));
	}
}
