<script>
  import { preferences } from '$lib/store.js';
  import AudioPlayer from './AudioPlayer.svelte';
  import {API_FQDN} from '$lib/constants.js';
  import { Styles } from 'sveltestrap';
  import { Col, Container, Row } from 'sveltestrap';
</script>

<Container>
  {#if $preferences.podcast}
  <Row cols={1}>
    <Col>
      <AudioPlayer src={$preferences.podcast}/>
    </Col>
  </Row>
  {/if}
  <Row cols={1}>
    <Col>
      <h1><a href='https://btcnews.today'>BTCNews.Today</a></h1>
      <p>Come for the news, stay for the low time preference.</p>
    </Col>
  </Row>
</Container>


