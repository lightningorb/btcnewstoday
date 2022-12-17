<script>
  import { Styles } from 'sveltestrap';
  import Nav from '../components/Nav.svelte';
  import Banner from '../components/Banner.svelte';
  import Footer from '../components/Footer.svelte';
  import { preferences } from '$lib/store.js';
  import { base } from '$app/paths';

  import { Col, Container, Row } from 'sveltestrap';
  import { get } from 'svelte/store'
  export const prerender = true;
  import '$lib/interceptors.js';

  let p = get(preferences);
  p.podcast = '';
  preferences.set(p);
  let theme_name = p.theme_name || 'light';

</script>

<svelte:head>
  <link rel="stylesheet" href="{base}/style-{theme_name}.css" />
</svelte:head>

<Styles/>

<Banner/>

<Nav/>

<Container>
  <Row cols={1}>
    <Col><slot></slot></Col>
  </Row>
</Container>

<Nav/>

<Footer />