import { API_FQDN } from "$lib/constants.js"
import {getUTCDateString} from '$lib/utils.js'

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch, params, slug}) {
  let AID = import.meta.env.VITE_AID;
  let SNAPSHOT = import.meta.env.VITE_SNAPSHOT;
  let date_param = '';
  let latest_snapshot = '';
  if (SNAPSHOT != undefined){
    date_param = `date=${SNAPSHOT}`;
    latest_snapshot = SNAPSHOT;
  } else {
    latest_snapshot = getUTCDateString();
  }
  let url = API_FQDN + '/api/articles/?' + date_param;
  const articles = await (await fetch(url)).json();  
  const podcasts = await (await fetch(API_FQDN + '/api/podcasts/?' + date_param)).json();
  const longforms = await (await fetch(API_FQDN + '/api/articles/?longform=true&' + date_param)).json();
  return {articles, podcasts, longforms, latest_snapshot};
}

