import { API_FQDN } from "$lib/constants.js"

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch}) {
  let res = await fetch(API_FQDN+'/api/articles/');
  const articles = await res.json();
  res = await fetch(API_FQDN+'/api/latest_snapshot/');
  const latest_snapshot = await res.json();
  return {articles, latest_snapshot};
}

