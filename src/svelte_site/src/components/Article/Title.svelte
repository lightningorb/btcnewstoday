<script type="text/javascript">
  import { Input } from 'sveltestrap';
  import Play from './Play.svelte';
  export let article;
  export let edit;
</script>

{#if edit}
    <h5>Title</h5>
    <Input type="textarea" bind:value={article.title}/>
{:else}
  <Play article={article}/>{(new Date(article.date*1000)).toISOString().slice(0, 10)} <span style='font-size: 1.3em;'><a target='_blank' href='{article.link}'>{article.title}</a></span>
{/if}