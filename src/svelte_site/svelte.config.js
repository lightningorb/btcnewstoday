import adapter from '@sveltejs/adapter-static';


/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
                  pages: 'build',
                  assets: 'build',
                  fallback: null,
                  precompress: false
		}),
        trailingSlash: 'always',
		alias: {
	      	components: 'src/components/', // can't use this for some reason, breaks the build
		},
		prerender: {
			// entries: ['/', '/about'],
			// crawl: false,
			origin: 'http://sveltekit-prerender',
			concurrency: 3,
			handleHttpError: ({ path, referrer, message }) => {
				console.log(path)
			    if (path.indexOf('/permalink') !== -1) {
			      return;
			    }

			    // otherwise fail the build
			    throw new Error(message);
			}
		},
		version: {
			name: Date.now().toString()
		},
		paths: {
			base: process.env.BN_SVELTE_BASE
		}
	},
};

export default config;
