<script>
  import ArticleDrafts from '$components/ArticleDrafts.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<ArticleDrafts articles={data.articles}/>
