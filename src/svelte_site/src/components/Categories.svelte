<script lang="ts">
	import { Form, FormGroup, FormText, Label } from 'sveltestrap';
	import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'sveltestrap';
	import axios from 'axios';
	import { API_FQDN } from '$lib/constants.js';
	let categories = [];
	export let category = '';

	axios
		.get(`${API_FQDN}/api/articles/categories/`)
		.then(function (response) {
			categories = response.data.sort();
		})
		.catch(function (error) {
			console.log(error);
			confirm('Error');
		});
</script>

<FormGroup>
	<Label for="category">Category</Label>
	<br />
	<Dropdown>
		<DropdownToggle caret>{category || 'Dropdown'}</DropdownToggle>
		<DropdownMenu>
			{#each categories as c}
				<DropdownItem on:click={() => (category = c)}>{c}</DropdownItem>
			{/each}
		</DropdownMenu>
	</Dropdown>
</FormGroup>
