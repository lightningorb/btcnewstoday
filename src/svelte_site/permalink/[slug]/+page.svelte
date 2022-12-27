<!-- <script>
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<h1>{data.title}</h1>
<div>{@html data.content}</div> -->
<script>
	import Latest from '../../../components/Latest.svelte';
	import Podcasts from '../../../components/Podcasts.svelte';
	import { Styles } from 'sveltestrap';
	import { Col, Container, Row } from 'sveltestrap';
	/** @type {import('./$types').PageData} */
	export let data;
</script>

<Container>
	<Row cols={{ lg: 2, md: 2, sm: 1 }}>
		<Col
			><Latest slug={data.slug} show_dates={false} articles={data.articles} title={'Latest'} /></Col
		>
		<Col>
			<Row cols={1}>
				<Col><Podcasts podcasts={data.podcasts} /></Col>
				<Col><Latest slug={data.slug} articles={data.longforms} title="Longform" /></Col>
			</Row>
		</Col>
	</Row>
</Container>
