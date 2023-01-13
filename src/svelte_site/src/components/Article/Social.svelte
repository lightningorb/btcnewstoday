<script>
	import { preferences } from '$lib/store.js';
	import { Input } from 'sveltestrap';
	import { Icon } from 'sveltestrap';
	import { Button } from 'sveltestrap';
	import { Col, Row } from 'sveltestrap';
	import { browser, dev } from '$app/environment';
	export let slug;
	export let article;
	export let edit;
	export let show;
	$: vclass = show ? 'social-showing' : 'social-hidden'
	let perm = `https://btcnews.today/${slug}/${article.id}#${article.id}`;
</script>

<Row>
	{#if edit}
		<Input type="textarea" bind:value={article.outlet} />
	{:else}
		<Col xs="8"
			><cite
				><a href={null} target="_blank" rel="noreferrer" on:click|preventDefault>{article.outlet}</a
				></cite
			></Col
		>
	{/if}
	<Col xs="2">
	<a target='_blank' rel='noreferrer' href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(article.title)}${encodeURIComponent('\n\n'+perm+'\n\n#bitcoin')}`}>
		<Button secondary size="sm" class={vclass}><Icon name="twitter" /></Button>
	</a>
	</Col>
	<Col xs="2"
		><a href={perm}
			><Button secondary size="sm" class={vclass}><Icon name="link" /></Button></a
		></Col
	>
</Row>
