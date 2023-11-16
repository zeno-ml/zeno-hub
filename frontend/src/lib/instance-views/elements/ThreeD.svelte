<script lang="ts">
	export let data: string;
</script>

<svelte:head>
	<script
		type="module"
		src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.0.1/model-viewer.min.js"
	></script>
</svelte:head>

<model-viewer
	alt="3D model for instance {data}"
	src={data}
	shadow-intensity="1"
	camera-controls
	touch-action="pan-y"
></model-viewer>
