<script lang="ts">
	export let renderedText: string;
</script>

<article class="prose break-all [&_a]:break-all [&_p]:break-all">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedText}
</article>
