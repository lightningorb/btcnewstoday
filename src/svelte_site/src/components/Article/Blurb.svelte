<script type="text/javascript">
	import { Input } from 'sveltestrap';
	export let article;
	export let edit;
</script>

{#if edit}
	<h5>Blurb</h5>
	<Input type="textarea" bind:value={article.blurb} />
{:else}
	<p>{article.blurb}</p>
{/if}
