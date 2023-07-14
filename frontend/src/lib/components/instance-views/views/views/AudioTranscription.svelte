<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: audioURL = entry['data'] as string;
</script>

<div id="container">
	<div class="box">
		<div style:display="flex">
			<audio controls src={audioURL}>
				<source src={audioURL} type={'audio/' + audioURL.split('.').at(-1)} />
			</audio>
		</div>
		<span class="label">label: </span><span class="value">
			{entry['label']}
		</span>
		{#if modelColumn && entry[modelColumn] !== undefined}
			<br />
			<span class="label">output: </span>
			<span class="value">{entry[modelColumn]} </span>
		{/if}
	</div>
</div>

<style>
	.label {
		font-size: 12px;
		color: rgba(0, 0, 0, 0.5);
		font-variant: small-caps;
	}
	.value {
		font-size: 12px;
	}
	.box {
		padding: 10px;
		border: 0.5px solid rgb(224, 224, 224);
		max-width: 400px;
	}
	#container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
	}

	:global(spectrogram canvas) {
		z-index: 0 !important;
	}
	:global(wave canvas) {
		z-index: 0 !important;
	}
	:global(wave) {
		z-index: 0 !important;
	}
</style>
