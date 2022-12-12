<script>
  import Login from '$components/Login.svelte';
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Login - BTCNews.today';
  });
</script>

<Login/>