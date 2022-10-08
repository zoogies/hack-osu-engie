<script>
	import './styles.css';

	export async function handle({ event, resolve }) {
    	return resolve(event, { ssr: false });
	}
</script>

<div class="app">
	<main>
		<slot />
	</main>
</div>

<style>
</style>
