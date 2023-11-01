<script lang="ts">
	import { mdiPlusCircle } from '@mdi/js';
	import { Icon } from '@smui/button';

	export let position: number;
	export let addElement: (elementIndex: number) => void;
	export let alwaysShow = false;
</script>

<button
	class="group h-6 w-full items-center justify-center transition"
	on:click={() => addElement(position)}
>
	<div
		class="h-0.5 w-full items-center justify-center bg-primary-dark
        {!alwaysShow ? 'hidden group-hover:flex' : 'flex'}
    "
	>
		<div class="bg-white">
			<Icon style="outline:none; width: 24px; height: 24px" tag="svg" viewBox="0 0 24 24">
				<path class="fill-primary-dark" d={mdiPlusCircle} />
			</Icon>
		</div>
	</div>
</button>
