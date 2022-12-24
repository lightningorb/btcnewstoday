<script>
  import Search from '../../components/Search.svelte';
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Search - BTCNews.today';
  });
</script>

<Search/>
