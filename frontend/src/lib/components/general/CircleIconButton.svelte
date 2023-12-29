<script lang="ts">
	import { Icon } from '@smui/button';

	export let icon: string;
	export let positioning: string = '';
</script>

<button
	class="{positioning} flex h-8 w-8 cursor-pointer items-center justify-center rounded-full border border-grey-light text-primary transition hover:bg-primary-mid"
	on:click
>
	<Icon tag="svg" viewBox="0 0 24 24" class="w-5 fill-primary">
		<path d={icon} />
	</Icon>
</button>
