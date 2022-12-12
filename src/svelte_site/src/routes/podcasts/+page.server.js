import { API_FQDN } from "$lib/constants.js"

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch}) {
  const res = await fetch(API_FQDN+'/api/podcasts/?is_draft=0');
  const podcasts = await res.json();
  return {podcasts};
}

