import { process } from 'node:process';
import { error } from '@sveltejs/kit';
import { RelayPool }  from 'nostr';

const relays = [
                'wss://nostream-production-539a.up.railway.app',
                "wss://relay.damus.io",
                "wss://nostr-pub.wellorder.net",
                'wss://nostr.xpersona.net',
                'wss://nostr-relay.freedomnode.com',
                'wss://relay.nostrmoto.xyz',
                'wss://nostrrelay.com',
                'wss://nostr1.tunnelsats.com'
            ]

 
/** @type {import('./$types').RequestHandler} */
export async function GET({ url }) {
  return new Promise((resolve, reject) => {
    const pool = RelayPool(relays)
    pool.on('open', relay => relay.subscribe("subid", {ids: [url.searchParams.get('note_id')]}));
    pool.on('eose', relay => relay.close());
    pool.on('event', (relay, sub_id, ev) => {
        relay.close()
        resolve(new Response(String(JSON.stringify(ev))));
    });
  });
}