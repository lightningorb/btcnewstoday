import { API_FQDN } from "$lib/constants.js"
import {getUTCDateString} from '$lib/utils.js'
export const prerender = true;

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
  return {articles};
}

