import { API_FQDN } from '$lib/constants.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
	const res = await fetch(API_FQDN + '/api/jobs/');
	const jobs = await res.json();
	return { jobs };
}
