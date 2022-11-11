<script>
  import { Styles } from 'sveltestrap';
  export let articles;
  export let title;
  import Article from './Article.svelte';
</script>

<Styles/>

<h1>{title}</h1>

{#each articles as article}
  <Article article={article}/>
  <hr/>
{/each}
