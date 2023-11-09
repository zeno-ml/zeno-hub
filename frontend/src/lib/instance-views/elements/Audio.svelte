<script lang="ts">
	export let data: string;
</script>

<audio controls src={data} class="my-2">
	<source src={data} type={'audio/' + `${data}`.split('.').at(-1)} />
</audio>
