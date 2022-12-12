import { API_FQDN } from "$lib/constants.js"

/** @type {import('./$types').PageLoad} */
export async function load({fetch, params}) {
  let slug = params.slug;
  const articles = await (await fetch(API_FQDN + `/api/articles/?snapshot=${params.slug}`)).json();
  const podcasts = await (await fetch(API_FQDN + `/api/podcasts/?snapshot=${params.slug}`)).json();
  const longforms = await (await fetch(API_FQDN + `/api/articles/?longform=true&snapshot=${params.slug}`)).json();
  return {articles, podcasts, longforms, slug};
}

