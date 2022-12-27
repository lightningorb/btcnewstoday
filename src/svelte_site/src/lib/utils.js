import axios from 'axios';
import { API_FQDN } from '$lib/constants.js';
import { preferences } from '$lib/store.js';
import { get } from 'svelte/store';

export function getUTCDateString() {
	const date = new Date();
	const year = date.getUTCFullYear();
	const month = date.getUTCMonth() + 1; // months are zero-indexed
	const day = date.getUTCDate();
	return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
}

export function logout() {
	let p = get(preferences);
	p.username = '';
	p.access_token = '';
	p.role = '';
	preferences.set(p);
}

export function save_user_info() {
	axios
		.get(`${API_FQDN}/api/users/me/`)
		.then((response) => {
			let p = get(preferences);
			console.log('save user info', p);
			p.role = response.data.role;
			p.username = response.data.username;
			preferences.set(p);
		})
		.catch((error) => {
			console.log(error);
		});
}

export function logged_in() {
	return get(preferences).access_token != '';
}

export function role_is_at_least(role) {
	const actual_role = get(preferences).role;
	const roles = {
		user: 0,
		contributor: 1,
		editor: 2,
		admin: 3
	};
	return roles[actual_role] >= roles[role];
}
