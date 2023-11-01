<script>
	import { page } from '$app/stores';
</script>

<div class="m-auto h-full bg-primary pt-20 text-center">
	<div class="m-auto flex w-96 flex-col items-center rounded-md bg-background p-10">
		<img src="/zeno.png" alt="zeno logo" class="w-10" />
		<h1 class="mt-4 text-xl font-semibold text-primary">{$page.status}</h1>
		<h1 class="text-xl text-primary">{$page.error.message}</h1>
	</div>
</div>
