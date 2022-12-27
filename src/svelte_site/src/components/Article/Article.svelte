<script>
	import { preferences } from '$lib/store.js';
	import axios from 'axios';
	import Contribute from './Contribute.svelte';
	import Blurb from './Blurb.svelte';
	import Title from './Title.svelte';
	import { Form, FormGroup, FormText, Label } from 'sveltestrap';
	import Tweets from './Tweets.svelte';
	import NostrNotes from './NostrNotes.svelte';
	import Social from './Social.svelte';
	import More from './More.svelte';
	import { Button } from 'sveltestrap';
	import { Popover } from 'sveltestrap';
	import { Input, Icon } from 'sveltestrap';
	import { API_FQDN } from '$lib/constants.js';
	import { Col, Container, Row } from 'sveltestrap';
	export let slug;
	export let article;
	export let show_dates = false;
	$: edit = false;
	let placement = 'bottom';
	let show = false;

	function save() {
		console.log(article);
		const headers = {
			'Content-Type': 'application/json'
		};
		let copy = JSON.parse(JSON.stringify(article));
		delete copy.tweets;
		delete copy.id;
		let body = JSON.stringify(copy);
		axios
			.post(`${API_FQDN}/api/update_article/${article.id}/`, body, { headers: headers })
			.then(function (response) {
				console.log(response);
				edit = false;
			})
			.catch(function (error) {
				console.log(error);
				confirm('Error');
			});
	}

	function _delete() {
		axios
			.post(`${API_FQDN}/api/delete_article/${article.id}/`)
			.then(function (response) {
				console.log(response);
				edit = false;
			})
			.catch(function (error) {
				console.log(error);
				confirm('Error');
			});
	}
</script>

<div id={article.id} />

<div class="container" on:mouseenter={() => show = true} on:mouseleave={() => show = false}>
	<div class="row">
		<div class="col-lg-12 pt-4 pt-lg-0">
			<!-- <span>{(new Date(article.date*1000)).toISOString()}</span> -->
			<Social {article} {edit} {slug} {show}/>
			{#if $preferences.show_images}
				<img src={article.image} class="article-hero-image float-end imgshadow" alt="" />
			{/if}
			<Title {article} {edit} {show_dates} />
			<Blurb {article} {edit} />
			<NostrNotes {article} />
			<Tweets {article} />
			{#if $preferences.access_token != ''}
				<Contribute article={article} bind:edit={edit}/>
			{/if}
		</div>
		<div style="text-align: left;" class="col-lg-5" />
	</div>
</div>

{#if edit}
	<FormGroup>
		<Input id="c1" type="checkbox" label="Longform" bind:checked={article.is_longform} />
		<Input id="c2" type="checkbox" label="Draft" bind:checked={article.is_draft} />
	</FormGroup>
	<button on:click={() => save()}>Save.</button>
	<button on:click={() => _delete()}>Delete.</button>
{/if}
