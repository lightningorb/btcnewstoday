<script>
	import { Styles } from 'sveltestrap';
	export let articles;
	export let slug;
	export let title;
	export let show_dates = false;
	import Article from './Article/Article.svelte';
</script>

<div class="section">
	{#if articles.length}
		<h2>{title}</h2>
	{/if}
	{#each articles as article, i}
		<Article {slug} {article} {show_dates} />
		{#if i < articles.length - 1}
			<hr />
		{/if}
	{/each}
</div>
