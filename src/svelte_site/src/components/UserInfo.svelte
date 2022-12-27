<script lang="ts">
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

	import { preferences } from '$lib/store.js';
	let tweets_added = 0;
	let tweets_approved = 0;
	let notes_added = 0;
	let notes_approved = 0;
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
			<span>Tweets added: {tweets_added}</span>
			<br />
			<span>Tweets approved: {tweets_approved}</span>
			<br />
			<span>Notes added: {notes_added}</span>
			<br />
			<span>Notes approved: {notes_approved}</span>
			<br />
		</CardText>
	</CardBody>
</Card>
