<script>
  import { Popover } from 'sveltestrap';
  export let article;
  export let edit;
</script>

<div style='padding-bottom: 10px;'><b>Tweets:</b>

{#each article.tweets as tweet}
  <Popover
    trigger="hover"
    placement="right"
    target={'id-'+tweet.id}
    title={'@'+tweet.username}
  >
    {tweet.text}
  </Popover>
  <a id={'id-'+tweet.id} target='_blank' href={`https://twitter.com/${tweet.username}/status/${tweet.id}`}>@{tweet.username}</a> <span style='width: 3px;'></span>
{/each}

</div>