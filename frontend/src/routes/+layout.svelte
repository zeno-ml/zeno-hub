<script lang="ts">
	import { browser } from '$app/environment';
	import { featureFlags } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import * as amplitude from '@amplitude/analytics-browser';
	import '../app.css';

	export let data;
	featureFlags.set({ ...zenoFeatureFlags, ...data.features });

	if (browser)
		amplitude.init('9e6755badfe6f970b509d3325a6a6678', {
			defaultTracking: true
		});
</script>

<div class="w-full h-full overflow-hidden">
	<slot />
</div>
