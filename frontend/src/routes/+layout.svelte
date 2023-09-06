<script lang="ts">
	import { browser } from '$app/environment';
	import * as amplitude from '@amplitude/analytics-browser';
	import '../app.css';

	if (browser)
		amplitude.init('9e6755badfe6f970b509d3325a6a6678', {
			defaultTracking: true
		});
</script>

<div class="w-full h-full overflow-hidden">
	<slot />
</div>
