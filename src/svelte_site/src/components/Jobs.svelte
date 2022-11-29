<script>
  import { Icon } from 'sveltestrap';
  import { preferences } from '$lib/store.js';
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";
  import Job from './Job.svelte';
  export let jobs;
  $: edit = false;

</script>

<Styles/>

<h2>Jobs</h2>

{#if $preferences.access_token != ''}
  {#if edit}
  {:else}
    <button on:click={() => edit=true}><Icon name="pencil-square"/></button>
  {/if}
{/if}


<Table striped>
  <thead>
    <tr>
      <th>Company</th>
      <th>Role</th>
    </tr>
  </thead>
  <tbody>
    {#each jobs as job}
      <Job job={job} edit={edit}/>
    {/each}
  </tbody>
</Table>