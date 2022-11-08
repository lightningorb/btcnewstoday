<script>
  import Latest from '../components/Latest.svelte';
  import Events from '../components/Events.svelte';
  import Podcasts from '../components/Podcasts.svelte';
  import Longform from '../components/Longform.svelte';
  import Jobs from '../components/Jobs.svelte';
  import { Styles } from 'sveltestrap';
  import { Col, Container, Row } from 'sveltestrap';
</script>

<Styles />

<Container>
  <Row cols={{ lg: 2, md: 2, sm: 1 }}>
    <Col><Latest/></Col>
    <Col>
      <Row cols={1}>
        <Col><Events/></Col>
        <Col><Podcasts/></Col>
      </Row>
    </Col>
  </Row>
  <Row cols={{ lg: 2, md: 2, sm: 1 }}>
    <Col><Longform/></Col>
    <Col>
      <Row cols={1}>
        <Col><Jobs/></Col>
      </Row>
    </Col>
  </Row>
</Container>