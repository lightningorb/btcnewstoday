<script lang="ts">
  import { preferences } from '$lib/store.js';
</script>

{#if $preferences.access_token != ''}
    logged in.
{/if}