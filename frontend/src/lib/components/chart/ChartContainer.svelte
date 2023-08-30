<script lang="ts">
	export let chartName: string;
</script>

<div class="ml-5 mt-5">
	<h2 class="mt-2 mb-3 text-grey-dark text-xl">
		{chartName}
	</h2>
	<div>
		<slot />
	</div>
</div>
