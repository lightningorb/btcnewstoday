<script lang="ts">
	import { preferences } from '$lib/store.js';
	import {
		Button,
		Card,
		CardBody,
		CardFooter,
		CardHeader,
		CardSubtitle,
		CardText,
		CardTitle
	} from 'sveltestrap';
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { API_FQDN } from '$lib/constants.js';
	let categories = [];
	export let category = '';
	let user_data = null;

	onMount(() => {
		axios
			.get(`${API_FQDN}/api/users/me/`)
			.then(function (response) {
				console.log(response);
				user_data = response.data;
			})
			.catch(function (error) {
				console.log(error);
				confirm('Error');
			});
	});

</script>

<Card class="mb-3">
	<CardHeader>
		<CardTitle class="text-capitalize">{$preferences.role} Info 👋</CardTitle>
	</CardHeader>
	<CardBody>
		<!-- <CardSubtitle>Card subtitle</CardSubtitle> -->
		<CardText>
			<span>Username: {$preferences.username}</span>
			<br />
			<span>Role: {$preferences.role}</span>
			<br />
			<span>Tweets added: {user_data ? user_data.num_tweets : 0}</span>
			<br />
			<span>Tweets approved: {user_data ? user_data.num_tweets_approved : 0}</span>
			<br />
			<span>Notes added: {user_data ? user_data.num_notes : 0}</span>
			<br />
			<span>Notes approved: {user_data ? user_data.num_notes_approved : 0}</span>
			<br />
			<span>Redeemable Sats: 丰{user_data ? user_data.redeemable_sats.toLocaleString() : 0}</span>
			<br />
			<span>Redeemed Sats: 丰{user_data ? user_data.redeemed_sats.toLocaleString() : 0}</span>
			<br />
		</CardText>
	</CardBody>
</Card>
