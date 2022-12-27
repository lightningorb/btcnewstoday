<script>
	import { Popover } from 'sveltestrap';
	export let article;
	article.tweets.sort((a, b) => a.id - b.id);
	let display = article.tweets.length;
</script>

{#if display}
	{#if article.tweets.length > 0}
		<b class="tweets-title">Tweets:</b>
	{/if}

	{#each article.tweets as tweet}
		<Popover trigger="hover" target={'id-' + tweet.id} title={'@' + tweet.username}>
			<p>{tweet.text}</p>
		</Popover>
		<a
			rel="noreferrer"
			class="tweet"
			id={'id-' + tweet.id}
			target="_blank"
			href={`https://twitter.com/${tweet.username}/status/${tweet.id}`}>@{tweet.username}</a
		> <span style="width: 3px;" />
	{/each}
{/if}
