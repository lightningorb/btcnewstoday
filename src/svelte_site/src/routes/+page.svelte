<script>
  import Latest from '../components/Latest.svelte';
  import Events from '../components/Events.svelte';
  import Podcasts from '../components/Podcasts.svelte';
  import Jobs from '../components/Jobs.svelte';
  import { Styles } from 'sveltestrap';
  import { Col, Container, Row } from 'sveltestrap';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Styles />

<Container>
  <Row cols={{ lg: 2, md: 2, sm: 1 }}>
    <Col><Latest show_dates={false} articles={data.articles} title={'Latest'}/></Col>
    <Col>
      <Row cols={1}>
        <Col><Podcasts podcasts={data.podcasts}/></Col>
        <Col><Latest articles={data.longforms} title='Longform'/></Col>
      </Row>
    </Col>
  </Row>
</Container>