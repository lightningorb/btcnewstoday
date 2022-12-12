<script>
  import Nav from '../components/Nav.svelte';
  import Banner from '../components/Banner.svelte';
  import Footer from '../components/Footer.svelte';
  import { preferences } from '$lib/store.js';

  import { Col, Container, Row } from 'sveltestrap';
  import { get } from 'svelte/store'
  export const prerender = true;
  import '$lib/interceptors.js';

  let p = get(preferences);
  p.podcast = '';
  preferences.set(p);

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