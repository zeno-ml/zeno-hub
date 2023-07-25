<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;
</script>

<svelte:head>
	<title>Register</title>
</svelte:head>

<div class="login-container">
	<div class="login-left">
		<h1>Zeno</h1>
		<div class="description-text">
			Zeno is an interactive platform that empowers developers to quickly discover, validate, and
			track model behaviors to evaluate and compare any AI systems. This is done through an
			intuitive, no-code interface supported by intelligent features such as automatic error
			discovery. In addition to making evaluation fast and repeatable, Zeno acts as a central hub
			that developer teams can use as a shared source of truth and guide for model development.
		</div>
	</div>
	<div class="login-right">
		<form method="POST" class="login-form" action="?/signup" use:enhance>
			<div class="form-container">
				<Textfield input$name="username" value={form ? `${form.name}` : ''} label="User name" />
				<Textfield
					input$name="email"
					type="email"
					value={form ? `${form.email}` : ''}
					label="Email address"
				/>
				<Textfield
					input$name="password"
					type="password"
					value={form ? `${form.password}` : ''}
					label="Password"
				/>
				<Textfield
					input$name="repeatPassword"
					type="password"
					value={form ? `${form.repeat}` : ''}
					label="Repeat password"
				/>
				<Button type="submit">Sign Up</Button>
				<div>
					Already have an account? <a href="/login">Log in now!</a>
				</div>
				{#if form?.error}
					<p>{form.error}</p>
				{/if}
			</div>
		</form>
	</div>
</div>

<style>
	.login-container {
		display: flex;
		height: 100%;
		width: 100%;
		background-color: var(--P2);
	}

	.login-left {
		width: 50%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: white;
		padding: 3em;
	}

	.description-text {
		font-size: larger;
		text-align: center;
	}

	.login-right {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 50%;
	}

	.login-form {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: white;
		padding: 3em;
		border-radius: 20px;
	}

	.form-container {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
</style>
