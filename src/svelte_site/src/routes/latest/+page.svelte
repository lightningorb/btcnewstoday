<script>
  import Latest from '../../components/Latest.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Latest - BTCNews.today';
  });
</script>

<Latest slug={data.latest_snapshot} articles={data.articles} title='Latest' show_dates={true}/>
