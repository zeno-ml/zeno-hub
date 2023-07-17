import { SlicesMetricsOrModels } from '$lib/zenoapi';
import MetricsEncodingDropdown from './chart-encoding/encoding-components/MetricsEncodingDropdown.svelte';
import MetricsEncodingMultiChoice from './chart-encoding/encoding-components/MetricsEncodingMultiChoice.svelte';
import ModelsEncodingDropdown from './chart-encoding/encoding-components/ModelsEncodingDropdown.svelte';
import ModelsEncodingMultiChoice from './chart-encoding/encoding-components/ModelsEncodingMultiChoice.svelte';
import SlicesEncodingDropdown from './chart-encoding/encoding-components/SlicesEncodingDropdown.svelte';
import SlicesEncodingMultiChoice from './chart-encoding/encoding-components/SlicesEncodingMultiChoice.svelte';

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
