<script lang="ts">
	export let document: { reference: string; text: string; score: string };
</script>

<div class="my-1 flex relative z-0 p-4 border border-grey-lighter">
	<div class="flex flex-col">
		<p class="text-grey whitespace-pre-wrap">
			<span class="font-semibold">score: </span>
			{document.score}
		</p>
		<p class="text-grey whitespace-pre-wrap">
			<span class="font-semibold">id: </span>
			{document.reference}
		</p>
		<p class="text-grey whitespace-pre-wrap">
			<span class="font-semibold">text: </span>
			{document.text}
		</p>
	</div>
</div>
