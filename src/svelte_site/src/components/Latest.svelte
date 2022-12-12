<script>
  import { Styles } from 'sveltestrap';
  export let articles;
  export let slug;
  export let title;
  export let show_dates = false;
  import Article from './Article/Article.svelte';
</script>

<Styles/>

<div class='section'>
  <h2>{title}</h2>
  {#each articles as article}
    <Article slug={slug} article={article} show_dates={show_dates}/>
    <hr/>
  {/each}
</div>
