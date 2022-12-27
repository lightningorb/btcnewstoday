<script>
	import { Icon } from 'sveltestrap';
	import { API_FQDN } from '$lib/constants.js';
	import axios from 'axios';
	export let job;
	export let edit;

	function _delete() {
		axios
			.post(`${API_FQDN}/api/delete_job/${job.id}/`)
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

<tr>
	<td>{job.company}</td>
	<td><a rel="noreferrer" target="_blank" href={job.link}>{job.role}</a></td>
	{#if edit}
		<button on:click={() => _delete()}><Icon name="trash" /></button>
	{/if}
</tr>
