<script>
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";
  export let jobs;

</script>

<Styles/>

<h2>Jobs</h2>

<Table striped>
  <thead>
    <tr>
      <th>Company</th>
      <th>Role</th>
    </tr>
  </thead>
  <tbody>
    {#each jobs as job}
    <tr>
      <td>{job.company}</td>
      <td><a target='_blank' href='{job.link}'>{job.role}</a></td>
    </tr>
    {/each}
  </tbody>
</Table>