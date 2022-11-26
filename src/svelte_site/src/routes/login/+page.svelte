<script>
  import Login from '../../components/Login.svelte';
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Login - ₿News.daily';
  });
</script>

<Login/>