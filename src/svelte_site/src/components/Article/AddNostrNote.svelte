<script lang="ts">
	import { API_FQDN } from '$lib/constants.js';
	import { InputGroup, InputGroupText, Input, Icon } from 'sveltestrap';
	import { Form, FormGroup, FormText, Label } from 'sveltestrap';
	import axios from 'axios';
	import { Button, Modal } from 'sveltestrap';
	import { Card, CardBody } from 'sveltestrap';

	let open = false;
	let text = '';

	export var article_id;

	async function get_note(note_id, author_pk) {
		console.log('get_note', author_pk, note_id);
		if (note_id == null || author_pk == null) return;
		if (note_id == '' || author_pk == '') return;
		console.log('getting');
		const res = await fetch(
			API_FQDN + `/api/third_party/nostr_note_text/?note_id=${note_id}&author_pk=${author_pk}`
		);
		const text = await res.json();
		return text;
	}

	function add_note(note_id, author_pk, text, username) {
		const headers = {
			'Content-Type': 'application/json'
		};
		let body = JSON.stringify({
			article_id,
			note_id,
			username,
			author_pk,
			text
		});
		axios
			.post('/api/nostr_notes/', body, { headers: headers })
			.then(function (response) {
				console.log(response);
				confirm('Looking good');
			})
			.catch(function (error) {
				console.log(error);
				confirm('Error');
			});
	}

	$: author_pk = '';
	$: username = '';
	$: note_id = '';
	$: note = '';
	// get_note(note_id, author_pk);

	const toggle = () => (open = !open);
</script>

<div>
	<button style='border: 0;' on:click={toggle}><img src="/add-nostr-note.png" style="width: 14px;" /></button> Add Note

	<Modal body header="Add Nostr Note" isOpen={open} {toggle}>
		<FormGroup>
			<Label for="link">Author Pubkey:</Label>
			<br />
			<Input type="textarea" name="text" id="link" bind:value={author_pk} />
			<Label for="link">Username:</Label>
			<br />
			<Input type="textarea" name="text" id="link" bind:value={username} />
			<br />
			<Label for="link">Note ID:</Label>
			<br />
			<Input type="textarea" name="text" id="link" bind:value={note_id} />
			<br />
			<Label for="link">Text:</Label>
			<br />
			<Input type="textarea" name="text" id="link" bind:value={text} />
			<br />
			<Button color="danger" on:click={() => add_note(note_id, author_pk, text, username)} size="sm"
				>Add Note</Button
			>
		</FormGroup>
	</Modal>
</div>
