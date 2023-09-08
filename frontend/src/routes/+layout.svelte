<script lang="ts">
	import { featureFlags } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import '../app.css';

	export let data;
	featureFlags.set({ ...zenoFeatureFlags, ...data.features });
</script>

<div class="w-full h-full overflow-hidden">
	<slot />
</div>
