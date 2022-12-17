<script>
  import { Styles } from 'sveltestrap';
  export let articles;
  export let slug;
  export let title;
  export let show_dates = false;
  import Article from './Article/Article.svelte';
</script>



<div class='section'>
  <h2>{title}</h2>
  {#each articles as article, i}
    <Article slug={slug} article={article} show_dates={show_dates}/>
    {#if i < articles.length -1}
      <hr/>
    {/if}
  {/each}
</div>
