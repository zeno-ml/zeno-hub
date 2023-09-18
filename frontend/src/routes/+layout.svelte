<script lang="ts">
	import { browser } from '$app/environment';
	import { PUBLIC_AMPLITUDE_API_KEY } from '$env/static/public';
	import { featureFlags } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import * as amplitude from '@amplitude/analytics-browser';
	import '../app.css';

	export let data;

	featureFlags.set({ ...zenoFeatureFlags, ...data.features });

	if (browser && PUBLIC_AMPLITUDE_API_KEY)
		amplitude.init(PUBLIC_AMPLITUDE_API_KEY, {
			defaultTracking: true
		});
</script>

<div class="w-full h-full overflow-hidden">
	<slot />
</div>
