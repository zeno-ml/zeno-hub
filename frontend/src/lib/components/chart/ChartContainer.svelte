<script lang="ts">
	export let chartName: string;
</script>

<div class="ml-5 mt-5">
	<h2 class="mb-3 mt-2 text-xl text-grey-dark">
		{chartName}
	</h2>
	<div>
		<slot />
	</div>
</div>
