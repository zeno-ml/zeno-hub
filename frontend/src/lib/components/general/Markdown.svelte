<script lang="ts">
	export let renderedText: string;
</script>

<div class="prose">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedText}
</div>
