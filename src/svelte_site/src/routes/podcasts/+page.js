import { API_FQDN } from "$lib/constants.js"
import {getUTCDateString} from '$lib/utils.js'

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch}) {
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
  const podcasts = await (await fetch(API_FQDN + '/api/podcasts/?' + date_param)).json();
  return {podcasts};
}

