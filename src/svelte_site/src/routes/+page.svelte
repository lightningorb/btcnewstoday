<script>
	import Latest from '../components/Latest.svelte';
	import Podcasts from '../components/Podcasts.svelte';
	import Ads from '../components/Ads.svelte';
	import { Styles } from 'sveltestrap';
	import { Col, Container, Row } from 'sveltestrap';
	/** @type {import('./$types').PageData} */
	export let data;
	import { page } from '$app/stores';

	let article = null;
	let AID = import.meta.env.VITE_AID;
	let snapshot = import.meta.env.VITE_SNAPSHOT;
	if (AID !== undefined) {
		let short = data.articles.filter((x) => x.id == AID)[0];
		let long = data.longforms.filter((x) => x.id == AID)[0];
		article = short || long;
	}
</script>

{#if import.meta.env.VITE_SNAPSHOT != undefined}
	<span> Snapshot: {import.meta.env.VITE_SNAPSHOT}</span>
{/if}

<svelte:head>
	{#if article != null}
		<meta name="viewport" content="width=device-width" />
		<meta property="og:url" content={`https://btcnews.today/${snapshot}/${AID}/#${AID}`} />
		<meta property="og:type" content="website" />
		<meta property="og:title" content={article.title} />
		<meta property="og:description" content={article.blurb} />
		{#if article.image != ''}
			<meta property="og:image" content={article.image} />
		{:else}
			<meta property="og:image" content="https://btcnews.today/favicon.png" />
		{/if}
	{:else}
		<meta name="viewport" content="width=device-width" />
		<meta property="og:url" content="https://btcnews.today" />
		<meta property="og:type" content="website" />
		<meta property="og:title" content="BTCNews.today" />
		<meta
			property="og:description"
			content="Come for the news, stay for the low time preference."
		/>
		<meta property="og:image" content="https://btcnews.today/favicon.png" />
	{/if}
</svelte:head>

<Styles />

<Container>
	<Row cols={{ lg: 2, md: 2, sm: 1 }}>
		<Col
			><Latest
				slug={data.latest_snapshot}
				show_dates={false}
				articles={data.articles}
				title={'Latest'}
			/></Col
		>
		<Col>
			<Row cols={1}>
				<Col><br /><Ads /></Col>
			</Row>

			<Row cols={1}>
				<Col
					><Latest
						slug={data.latest_snapshot}
						show_dates={false}
						articles={data.techdev}
						title={'Tech & Dev'}
					/></Col
				>
			</Row>
			<Row cols={1}>
				<Col><Podcasts podcasts={data.podcasts} /></Col>
			</Row>
			<Row cols={1}>
				<Col><Latest slug={data.latest_snapshot} articles={data.longforms} title="Longform" /></Col>
			</Row>
		</Col>
	</Row>
</Container>

<br />
