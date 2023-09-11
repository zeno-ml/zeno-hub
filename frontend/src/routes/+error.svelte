<script>
	import { page } from '$app/stores';
</script>

<div class="m-auto text-center pt-20 bg-primary h-full">
	<div class="p-10 bg-background w-96 m-auto flex flex-col items-center rounded-md">
		<img src="/zeno.png" alt="zeno logo" class="w-10" />
		<h1 class="mt-4 text-xl font-semibold text-primary">{$page.status}</h1>
		<h1 class="text-xl text-primary">{$page.error.message}</h1>
	</div>
</div>
