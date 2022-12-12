<script>
  import { Popover } from 'sveltestrap';
  export let article;
  article.tweets.sort((a, b) => a.id - b.id);
</script>

<div>

{#if article.tweets.length > 0}
  <b>Tweets:</b>
{/if}

{#each article.tweets as tweet}
  <Popover
    trigger="hover"
    placement="right"
    target={'id-'+tweet.id}
    title={'@'+tweet.username}
  >
    {tweet.text}
  </Popover>
  <a rel="noreferrer" class='tweet' id={'id-'+tweet.id} target='_blank' href={`https://twitter.com/${tweet.username}/status/${tweet.id}`}>@{tweet.username}</a> <span style='width: 3px;'></span>
{/each}

</div>