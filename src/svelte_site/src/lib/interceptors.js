import { get } from 'svelte/store';
import { preferences } from '$lib/store.js';
import axios from 'axios';

axios.interceptors.request.use(
	(config) => {
		config.headers['Authorization'] = `Bearer ${get(preferences).access_token}`;
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);
