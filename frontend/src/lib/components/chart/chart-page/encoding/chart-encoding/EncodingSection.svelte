<script lang="ts">
	export let title = '';
</script>

<div class="mb-3">
	<h4 class="mb-2 font-semibold">{title}</h4>
	<slot name="parameters" />
	<div class="mt-2">
		<slot name="component" />
	</div>
</div>
