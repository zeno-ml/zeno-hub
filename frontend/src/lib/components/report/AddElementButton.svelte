<script lang="ts">
	import { mdiPlusCircle } from '@mdi/js';
	import { Icon } from '@smui/button';

	export let position: number;
	export let addElement: (elementIndex: number) => void;
	export let alwaysShow = false;
</script>

<button
	class="transition w-full h-6 justify-center items-center group"
	on:click={() => addElement(position)}
>
	<div
		class="justify-center items-center h-1 w-full bg-primary-dark
        {!alwaysShow ? 'group-hover:flex hidden' : 'flex'}
    "
	>
		<div class="bg-white">
			<Icon style="outline:none; width: 24px; height: 24px" tag="svg" viewBox="0 0 24 24">
				<path class="fill-primary-dark" d={mdiPlusCircle} />
			</Icon>
		</div>
	</div>
</button>
