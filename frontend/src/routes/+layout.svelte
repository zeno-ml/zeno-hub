<script lang="ts">
	import { browser } from '$app/environment';
	import { env } from '$env/dynamic/public';
	import { featureFlags } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import * as amplitude from '@amplitude/analytics-browser';
	import '../app.css';

	export let data;

	featureFlags.set({ ...zenoFeatureFlags, ...data.features });

	if (browser && env.PUBLIC_AMPLITUDE_API_KEY)
		amplitude.init(env.PUBLIC_AMPLITUDE_API_KEY, {
			defaultTracking: true
		});
</script>

<div class="w-full h-full overflow-hidden">
	<slot />
</div>
