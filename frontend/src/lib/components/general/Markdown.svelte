<script lang="ts">
	export let renderedText: string;
</script>

<article
	class="prose break-all [&_a]:break-all [&_p]:break-all [&_p]:whitespace-pre-wrap max-w-none"
>
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedText}
</article>
