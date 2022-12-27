<script>
	import {
		Card,
		CardBody,
		CardFooter,
		CardHeader,
		CardSubtitle,
		CardText,
		CardTitle
	} from 'sveltestrap';

	import { API_FQDN } from '$lib/constants.js';
	import { Form, FormGroup, FormText, Label } from 'sveltestrap';
	import { InputGroup, InputGroupText, Input } from 'sveltestrap';
	import axios from 'axios';
	let term = null;
	let res = [];

	function onkeypress(x) {
		axios.get(API_FQDN + '/api/meta/search/?term=' + term).then(function (response) {
			if (response.data != undefined) {
				res = response.data;
			}
		});
	}

	let timer;

	const debounce = (v) => {
		clearTimeout(timer);
		timer = setTimeout(() => {
			term = v;
			onkeypress(v);
		}, 500);
	};
</script>

<h1>Search</h1>

<Input id="search-box" on:keyup={({ target: { value } }) => debounce(value)} autocomplete="off" />

<br />

{#each res as r}
	<Card>
		<CardBody>
			<CardSubtitle
				><a target="_blank" ref="noreferrer" href="https://btcnews.today/{r.date}/{r.id}#{r.id}"
					>{r.title}</a
				></CardSubtitle
			>
			<CardText>
				{@html r.highlights}
			</CardText>
		</CardBody>
	</Card>
	<br />
{/each}
<br />
