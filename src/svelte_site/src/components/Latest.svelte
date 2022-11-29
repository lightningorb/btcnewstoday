<script>
  import { Styles } from 'sveltestrap';
  export let articles;
  export let title;
  import Article from './Article/Article.svelte';
</script>

<Styles/>

<div class='section'>
  <h2>{title}</h2>
  {#each articles as article}
    <Article article={article}/>
    <hr/>
  {/each}
</div>
