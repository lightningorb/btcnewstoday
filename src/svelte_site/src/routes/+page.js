import { API_FQDN } from "$lib/constants.js"

/** @type {import('./$types').PageLoad} */
export async function load({fetch, params}) {
  const articles = await (await fetch(API_FQDN + '/api/articles/')).json();
  const events = await (await fetch(API_FQDN + '/api/events/')).json();
  const podcasts = await (await fetch(API_FQDN + '/api/podcasts/')).json();
  const longforms = await (await fetch(API_FQDN + '/api/articles/?longform=true')).json();
  const jobs = await (await fetch(API_FQDN + '/api/jobs/')).json();
  return {articles, events, podcasts, longforms, jobs};
}

