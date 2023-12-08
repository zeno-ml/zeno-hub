<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { metrics, models } from '$lib/stores';

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}
</script>

<h1>Home</h1>
