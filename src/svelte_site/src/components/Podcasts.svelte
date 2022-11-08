<script>
  import { Table } from 'sveltestrap';
  import { Styles } from 'sveltestrap';
</script>

<Styles/>

<h2>Podcasts</h2>

<Table striped>
  <thead>
    <tr>
      <th>#</th>
      <th>Date</th>
      <th>Name</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Nov 4-7</td>
      <td>Breakpoint</td>
      <td>Lisbon</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Nov 10</td>
      <td>VMWare Explore Europe</td>
      <td>Lapland Europe</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Nov 12</td>
      <td>The Boat</td>
      <td>Early Bird</td>
    </tr>
  </tbody>
</Table>