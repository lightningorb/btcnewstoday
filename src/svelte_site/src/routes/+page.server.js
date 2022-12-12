import { API_FQDN } from "$lib/constants.js"
export const prerender = true;

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch, params}) {
  const articles = await (await fetch(API_FQDN + '/api/articles/')).json();
  const events = await (await fetch(API_FQDN + '/api/events/')).json();
  const podcasts = await (await fetch(API_FQDN + '/api/podcasts/')).json();
  const longforms = await (await fetch(API_FQDN + '/api/articles/?longform=true')).json();
  const jobs = await (await fetch(API_FQDN + '/api/jobs/')).json();
  const latest_snapshot = await (await fetch(API_FQDN+'/api/latest_snapshot/')).json();
  return {articles, events, podcasts, longforms, jobs, latest_snapshot};
}

