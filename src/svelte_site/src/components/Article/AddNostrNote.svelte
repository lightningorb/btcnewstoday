<script lang="ts">
	import { API_FQDN } from '$lib/constants.js';
	import { InputGroup, InputGroupText, Input, Icon } from 'sveltestrap';
	import { Form, FormGroup, FormText, Label } from 'sveltestrap';
	import axios from 'axios';
	import { Button, Modal } from 'sveltestrap';
	import { Card, CardBody } from 'sveltestrap';

	let open = false;
	export let isOpen;
	let text = '';
	let host =  API_FQDN.slice(0, API_FQDN.length-5);
	console.log(host);

	export var article_id;
	export let sats_for_note;

	async function get_note(note_id) {
		if (note_id == null) return;
		const decoded = bech32.decode(note_id)
		const bytes = fromWords(decoded.words)
		const value = hex_encode(bytes)
		console.log('getting');
		const res = await fetch(API_FQDN+`/jsapi/nostr?note_id=${value}`);
		const text = await res.json();
		return text;
	}

	function astral_re(link) {
		var rx = /(note1.*)/g;
		var arr = rx.exec(link);
		if (arr && arr.length){
			console.log(arr[1]);
			return arr[1];
		}
	}

	function add_note(note_id, text, username) {
		const headers = {
			'Content-Type': 'application/json'
		};
		let body = JSON.stringify({
			article_id,
			note_id,
			username,
			text
		});
		axios
			.post(API_FQDN+'/api/nostr_notes/', body, { headers: headers })
			.then(function (response) {
				console.log(response);
				confirm('Looking good');
			})
			.catch(function (error) {
				console.log(error);
				confirm('Error');
			});
	}


	function hex_char(val)
	{
		if (val < 10)
			return String.fromCharCode(48 + val)
		if (val < 16)
			return String.fromCharCode(97 + val - 10)
	}

	function hex_encode(buf)
	{
		var str = ""
		for (let i = 0; i < buf.length; i++) {
			const c = buf[i]
			str += hex_char(c >> 4)
			str += hex_char(c & 0xF)
		}
		return str
	}

	$: username = '';
	$: link = '';
	$: note_id = astral_re(link);
	$: note = get_note(note_id);

	const toggle = () => {
		open = !open;
		if (!open)
			setTimeout(() => isOpen = false, 1000)
	};
</script>

<div>
	<button style='border: 0;' on:click={toggle}><img src="/add-nostr-note.png" style="width: 14px;" /> Add Note </button> {#if sats_for_note}<span class='dorrar'>$</span>{/if}

	<Modal body style='--bs-popover-zindex: 2000 !important;'  header="Add Note" isOpen={open} {toggle}>
		<style>
			.fade {
				background: transparent;
			}
			.modal {
				--bs-modal-zindex: 2000;
			}
		</style>
		<FormGroup>
			<Label for="link">Note:</Label>
			<br />
			<Input type="textarea" name="text" id="link" bind:value={link} />
			<br />
			<Label for="link">Username:</Label>
			<br />
			<Input type="textarea" name="text" id="username" bind:value={username} />
			<br />
			{#if note_id}
				{#await note}
					<p>fetching note...</p>
				{:then note}
					<Card>
						<CardBody>{note.content}</CardBody>
					</Card>
					<br />
					<Button color="danger" on:click={() => add_note(note_id, note.content, username)} size="sm">Add Note</Button>
				{/await}
			{/if}
		</FormGroup>
	</Modal>
</div>
