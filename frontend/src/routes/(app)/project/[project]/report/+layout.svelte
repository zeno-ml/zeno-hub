<script lang="ts">
	import { charts } from '$lib/stores.js';

	export let data;

	$: {
		charts.set(data.charts);
	}
</script>

<slot />
