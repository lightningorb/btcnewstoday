import adapter from '@sveltejs/adapter-node';


/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
          ssr: {
            noExternal: ['@popperjs/core']
          }
        }),
        paths: {
          base: process.env.BN_SVELTE_BASE
        }
    }
};

export default config;
