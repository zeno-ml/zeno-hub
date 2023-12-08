<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { metrics, models } from '$lib/stores';

	export let data;

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}

	console.log(data.elements);
</script>

<h1>Home</h1>
