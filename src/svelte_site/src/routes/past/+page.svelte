<script>
  import Past from '../../components/Past.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Past - BTCNews.today';
  });
</script>

<Past articles={data.articles} title='Past'/>
