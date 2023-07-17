import { SlicesMetricsOrModels } from '$lib/zenoapi';
import MetricsEncodingDropdown from './MetricsEncodingDropdown.svelte';
import MetricsEncodingMultiChoice from './MetricsEncodingMultiChoice.svelte';
import ModelsEncodingDropdown from './ModelsEncodingDropdown.svelte';
import ModelsEncodingMultiChoice from './ModelsEncodingMultiChoice.svelte';
import SlicesEncodingDropdown from './SlicesEncodingDropdown.svelte';
import SlicesEncodingMultiChoice from './SlicesEncodingMultiChoice.svelte';

export const EncodingMap = {
	[SlicesMetricsOrModels.SLICES]: {
		fixed: SlicesEncodingDropdown,
		multi: SlicesEncodingMultiChoice
	},
	[SlicesMetricsOrModels.METRICS]: {
		fixed: MetricsEncodingDropdown,
		multi: MetricsEncodingMultiChoice
	},
	[SlicesMetricsOrModels.MODELS]: {
		fixed: ModelsEncodingDropdown,
		multi: ModelsEncodingMultiChoice
	}
};
