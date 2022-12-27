<script>
	import Article from './Article/Article.svelte';
	import { Table, Styles } from 'sveltestrap';
	import { onMount } from 'svelte';
	export let articles;
</script>

<h2>Article Drafts</h2>

{#each articles as article}
	<Article {article} show_dates={true} />
	<br />
	<hr />
{/each}
