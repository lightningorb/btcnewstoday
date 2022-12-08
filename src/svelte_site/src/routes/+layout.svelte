<script>
  /** @type {import('./$types').LayoutData} */
  export let data;
  import Nav from '../components/Nav.svelte';
  import Banner from '../components/Banner.svelte';
  import Footer from '../components/Footer.svelte';
  import { Col, Container, Row } from 'sveltestrap';
  export const prerender = true;
  import '$lib/interceptors.js';

</script>

<Banner/>

<Nav/>

<Container>
  <Row cols={1}>
    <Col><slot></slot></Col>
  </Row>
</Container>

<Nav/>

<Footer />