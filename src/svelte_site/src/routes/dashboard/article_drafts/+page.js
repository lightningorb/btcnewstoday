import { API_FQDN } from "$lib/constants.js"

/** @type {import('./$types').PageLoad} */
export async function load({fetch}) {
  const res = await fetch(API_FQDN+'/api/articles/?is_draft=true&limit=200');
  const articles = await res.json();
  return {articles};
}

