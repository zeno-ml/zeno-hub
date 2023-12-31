<script lang="ts">
	import { browser } from '$app/environment';
	import { onNavigate } from '$app/navigation';
	import { env } from '$env/dynamic/public';
	import Tooltip from '$lib/components/general/Tooltip.svelte';
	import { featureFlags, tooltipState } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import * as amplitude from '@amplitude/analytics-browser';
	import '../app.postcss';

	export let data;

	featureFlags.set({ ...zenoFeatureFlags, ...data.features });

	if (browser && env.PUBLIC_AMPLITUDE_API_KEY)
		amplitude.init(env.PUBLIC_AMPLITUDE_API_KEY, {
			defaultTracking: true
		});

	onNavigate(() => {
		tooltipState.set({
			hover: false,
			mousePos: { x: 0, y: 0 },
			text: undefined
		});
	});
</script>

<div class="h-full w-full overflow-hidden">
	<slot />
	<Tooltip></Tooltip>
</div>
