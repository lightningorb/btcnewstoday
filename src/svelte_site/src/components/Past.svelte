<script>
  import { Styles } from 'sveltestrap';
  export let articles;
  export let title;
  import PastArticle from './PastArticle.svelte';
</script>

<Styles/>

<h1>{title}</h1>

{#each articles as [date, arts]}
    <h5>{(new Date(date*1000)).toISOString().slice(0, 10)}</h5>>
    {#each arts as article}
      <PastArticle article={article}/>
      <hr/>
    {/each}
{/each}
