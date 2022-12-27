import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			ssr: {
				noExternal: ['@popperjs/core']
			}
		})
	}
};

export default config;
