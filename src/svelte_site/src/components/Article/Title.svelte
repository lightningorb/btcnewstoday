<script type="text/javascript">
	import { Input } from 'sveltestrap';
	import Play from './Play.svelte';
	export let article;
	export let edit;
	export let show_dates = false;
</script>

{#if edit}
	<h5>Title</h5>
	<Input type="textarea" bind:value={article.title} />
{:else}
	{#if show_dates}
		<span>{new Date(article.date * 1000).toISOString().slice(0, 10)}</span>
	{/if}
	<span style="font-size: 1.3em;"
		><a rel="noreferrer" target="_blank" href={article.link} class="title">{article.title}</a></span
	>
{/if}
