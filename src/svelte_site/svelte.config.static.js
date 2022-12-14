// import adapter from '@sveltejs/adapter-auto';
import adapter from '@sveltejs/adapter-static';
// import adapter from '@sveltejs/adapter-node';
import preprocess from 'svelte-preprocess';


/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: preprocess({
		replace: [
		        	[/process\.env\.NODE_ENV/g, JSON.stringify(process.env.NODE_ENV)],
		        	[/process\.env\.IS_STATIC/g, JSON.stringify(process.env.IS_STATIC)],
		        	[/process\.env\.BLAH/g, JSON.stringify(process.env.BLAH)]
		          ]
	}),
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
