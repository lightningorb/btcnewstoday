<script>
  /** @type {import('./$types').LayoutData} */
  export let data;
  import Nav from '../components/Nav.svelte';
  import { Col, Container, Row } from 'sveltestrap';
</script>

<Nav/>

<Container>
  <Row cols={1}>
    <Col><slot></slot></Col>
  </Row>
</Container>

<Nav/>
