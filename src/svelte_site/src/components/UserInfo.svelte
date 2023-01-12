<script lang="ts">
	import { preferences } from '$lib/store.js';
    import Time from "svelte-time";
    import { Alert } from 'sveltestrap';
    import { Lottie } from 'lottie-svelte';
	import { Toast, ToastBody, ToastHeader } from 'sveltestrap';
	import {
		Button,
		Card,
		CardBody,
		CardFooter,
		Table,
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
	let success = false;
	let withdrawals = [];
    let error = null;

	const withdraw = (() => {
		success = true;
		axios
			.post(`${API_FQDN}/api/bounty/withdraw/`)
			.then(function (response) {
				console.log(response);
			})
			.catch(function (err) {
				console.log(err);
				if (err.response && err.response.data && err.response.data.detail)
					error = err.response.data.detail
				else
					error = err
			});
	});
	function get_info(){
		axios
			.get(`${API_FQDN}/api/users/me/`)
			.then(function (response) {
				// console.log(response);
				user_data = response.data;
			})
			.catch(function (error) {
				console.log(error);
				// confirm('Error');
			});
		axios
			.get(`${API_FQDN}/api/bounty/withdrawals/`)
			.then(function (response) {
				// console.log(response.data);
				withdrawals = response.data;
			})
			.catch(function (error) {
				console.log(error);
				// confirm('Error');
			});
	}
	onMount(() => {
		get_info()
	});

    export let id;
    let progress = {}
    let poller
    const setupPoller = (id) => {
        if (poller) {
            clearInterval(poller)
        }
        poller = setInterval(doPoll(id), 2000)
    }
    const doPoll = (id) => async () => {
    	get_info();
        progress[id] = await new Promise(resolve => setTimeout(() => {
            resolve((progress[id] || 0) + 1)
        }, 1000))
    }
    $: setupPoller(id)
</script>

{#if user_data}

<style>
	svg {
		width: 50px !important;
	}
</style>

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
			<span>Tweets added: {user_data.num_tweets}</span>
			<br />
			<span>Tweets approved: {user_data.num_tweets_approved}</span>
			<br />
			<span>Notes added: {user_data.num_notes}</span>
			<br />
			<span>Notes approved: {user_data.num_notes_approved}</span>
			<br />
			<span>Redeemable Sats: 丰{user_data.redeemable_sats.toLocaleString()}</span>
			<br />
			<span>Redeemed Sats: 丰{user_data.redeemed_sats.toLocaleString()}</span>
			<br />
			<span>LN Address: {user_data.ln_address}</span>
			<br />
			<br />
			{#if user_data && user_data.redeemable_sats > 0}
				<!-- {#if !success} -->
					<Button on:click={withdraw}>Withdraw 丰{user_data.redeemable_sats}</Button>
				<!-- {:else} -->
					<!-- <span class='lottie-anim'><Lottie path="/thunder.json" speed={1} loop={false}/></span> -->
				<!-- {/if} -->
			{/if}
			{#if error}
				<br/>
				<br/>
				<Alert danger>
				    {error}
				</Alert>
			{/if}
			<span class='lottie-anim'><Lottie path="/waiting.json" speed={1} loop={true}/></span>
			<Table bordered>
			  <thead>
			    <tr>
			      <th>Amount</th>
			      <th>Date</th>
			      <th>Status</th>
			      <th>Address</th>
			      <th>Payment Hash</th>
			    </tr>
			  </thead>
			  <tbody>
			  	{#each withdrawals as w}
			    <tr>
			      <th scope="row">丰{w.amount_msat/1000}</th>
			      <td><Time id={w.id} relative live={1000} timestamp={w.date * 1000}/></td>
			      <!-- <td>{w.date}</td> -->
			      <td>{w.status}</td>
			      <td>{w.ln_address.slice(0, 10)}..</td>
			      <td>{w.payment_hash.slice(0, 10)}..</td>
			    </tr>
			    {/each}
			  </tbody>
			</Table>
		</CardText>
	</CardBody>
</Card>
{/if}