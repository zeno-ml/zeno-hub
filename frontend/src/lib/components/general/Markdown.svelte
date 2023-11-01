<script lang="ts">
	export let renderedText: string;
</script>

<article class="[&_a]:break-word prose max-w-none [&_p]:whitespace-pre-wrap">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedText}
</article>
