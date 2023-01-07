<script>
    import { role_is_at_least } from '$lib/utils.js';
    import Tweet from './Tweet.svelte';
	export let article;
	article.tweets.sort((a, b) => a.date - b.date);
	var tweets = role_is_at_least('editor') ? article.tweets : article.tweets.filter((a) => a.approved);
	let display = tweets.length;
</script>

{#if display}
	{#if tweets.length > 0}
		<b class="tweets-title">Tweets:</b>
	{/if}

	{#each tweets as tweet}
		<Tweet tweet={tweet}/>
	{/each}
{/if}
