<script lang="ts">
	import axios from 'axios';
	import { API_FQDN } from '$lib/constants.js';
	import { InputGroup, InputGroupText, Input } from 'sveltestrap';
	import { logout } from '$lib/utils.js';
	import { Alert, Button } from 'sveltestrap';
	import { get } from 'svelte/store';
	import { preferences } from '$lib/store.js';
	import { save_user_info } from '$lib/utils.js';

	const colors = ['primary'];

	let reg_alert_visible = false;
	let reg_alert_message = '';
	let login_alert_visible = false;
	let username = '';
	let password = '';
	let twitter_username = '';

	let rusername = '';
	let rpassword = '';

	function login() {
		login_alert_visible = false;
		const headers = {
			'Content-Type': 'application/json'
		};
		var bodyFormData = new FormData();
		bodyFormData.append('username', username);
		bodyFormData.append('password', password);
		const request = {
			method: 'post',
			url: `${API_FQDN}/token/`,
			data: bodyFormData,
			headers: { 'Content-Type': 'multipart/form-data' }
		};

		axios(request)
			.then((response) => {
				let p = get(preferences);
				console.log(p);
				p.access_token = response.data.access_token;
				p.role = response.data.role;
				preferences.set(p);
				save_user_info();
			})
			.catch((error) => {
				login_alert_visible = true;
			});
	}

	function register() {
		reg_alert_visible = false;
		const headers = {
			'Content-Type': 'application/json'
		};
		let body = JSON.stringify({ username:rusername, password:rpassword, twitter_username:twitter_username });
		axios
			.post(`${API_FQDN}/api/register/`, body, { headers: headers })
			.then(function (response) {
				let p = get(preferences);
				p.access_token = response.data.access_token;
				preferences.set(p);
				save_user_info();
			})
			.catch(function (error) {
				reg_alert_message = error.response.data.detail;
				reg_alert_visible = true;
			});
	}
</script>

{#if $preferences.access_token != ''}
	<h1>You're logged in</h1>

	<button on:click={logout}>Log out</button>
{:else}
	<h1>Login</h1>
	<InputGroup>
		<table width="400px">
			<tr>
				<td>
					<InputGroupText>username</InputGroupText>
				</td>
				<td>
					<Input placeholder="username" bind:value={username} />
				</td>
			</tr>
			<tr>
				<td>
					<InputGroupText>password</InputGroupText>
				</td>
				<td>
					<Input type='password' placeholder="password" bind:value={password} />
				</td>
			</tr>
		</table>
	</InputGroup>
	<br />
	<button on:click={login}>Log in</button>
	<br />
	<br />
	<Alert color="danger" isOpen={login_alert_visible} toggle={() => (login_alert_visible = false)}>
		Error: <code>Could not log in</code>.
	</Alert>

	<h1>Register</h1>

	<InputGroup>
		<table width="400px">
			<tr>
				<td>
					<InputGroupText>Username</InputGroupText>
				</td>
				<td>
					<Input placeholder="username" bind:value={rusername} />
				</td>
			</tr>
			<tr>
				<td>
					<InputGroupText>Password</InputGroupText>
				</td>
				<td>
					<Input type='password' placeholder="password" bind:value={rpassword} />
				</td>
			</tr>
			<tr>
				<td>
					<InputGroupText>Twitter Username</InputGroupText>
				</td>
				<td>
					<Input placeholder="my_twitter_un" bind:value={twitter_username} />
				</td>
			</tr>
		</table>
	</InputGroup>

	<Alert color="danger" isOpen={reg_alert_visible} toggle={() => (reg_alert_visible = false)}>
		Error: <code>{reg_alert_message}</code>.
	</Alert>

	<br />

	<button on:click={register}>Register</button>

	<!--   <Alert Warning>
    <h4 class="alert-heading text-capitalize">primary</h4>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    <a href="#todo" class="alert-link">
      Also, alert-links are colored to match
    </a>
    .
  </Alert> -->

	<br />
	<br />
	{#each colors as color}
		<Alert {color}>
			<h4 class="alert-heading text-capitalize">Note: Twitter Username ✍</h4>
			We'll DM your Twitter user id in case you need a <b>password reset</b>.
		</Alert>
	{/each}
{/if}

<br />
<br />
