import { API_FQDN } from '$lib/constants.js';
import { getUTCDateString } from '$lib/utils.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
	let SNAPSHOT = import.meta.env.VITE_SNAPSHOT;
	let date_param = '';
	let latest_snapshot = '';
	if (SNAPSHOT != undefined) {
		date_param = `date=${SNAPSHOT}`;
		latest_snapshot = SNAPSHOT;
	} else {
		latest_snapshot = getUTCDateString();
	}
	const url = API_FQDN + '/api/podcasts/?' + date_param;
	const podcasts = await (await fetch(url)).json();
	return { podcasts };
}
