<script>
	import { Button } from 'sveltestrap';
	import { Col, Row } from 'sveltestrap';
	import { Icon } from 'sveltestrap';
	export let article;
</script>

<span>{new Date(article.date * 1000).toISOString().slice(11, 16)}</span>
<cite><a rel="noreferrer" target="_blank" href="https://bloomberg.com">{article.outlet}</a></cite>
<span style="font-size: 1em;"
	><a rel="noreferrer" target="_blank" href={article.link}>{article.title}</a></span
><br />
