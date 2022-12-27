import Fa from 'svelte-fa/src/fa.svelte';
import { faList, faPenRuler, faUserDoctor, faUser, faGear, faNewspaper, faPodcast, faCalendar } from '@fortawesome/free-solid-svg-icons/index.js';

/** @type {import('./$types').LayoutLoad} */
export function load() {
	return {
		sections: [
			{ slug: 'profile', title: 'Profile', auth: false, roles: ['user'], icon: faUser },
			{ slug: 'prefs', title: 'Prefs', auth: false, roles: ['user'], icon: faGear },
			{ title: '<hr/>', auth: false, roles: ['user'] },
			{ slug: 'add_article', title: 'Add Article', auth: true, roles: ['admin'] , icon: faNewspaper },
			{ slug: 'add_podcast', title: 'Add Podcast', auth: true, roles: ['admin'], icon: faPodcast},
			{ slug: 'add_event', title: 'Add Event', auth: true, roles: ['admin'], icon: faCalendar},
			{ slug: 'add_job', title: 'Add Job', auth: true, roles: ['admin'], icon: faUserDoctor },
			{ slug: 'article_drafts', title: 'View Article Drafts', auth: true, roles: ['admin'], icon:faPenRuler},
			{ slug: 'podcast_drafts', title: 'View Podcast Drafts', auth: true, roles: ['admin'], icon:faList}
		]
	};
}

export const prerender = true;
export const csr = true;
export const ssr = true;
