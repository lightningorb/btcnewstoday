import { API_FQDN } from '$lib/constants.js';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
	const res = await fetch(API_FQDN + '/api/podcasts/?is_draft=true&limit=1000');
	const podcasts = await res.json();
	return { podcasts };
}
