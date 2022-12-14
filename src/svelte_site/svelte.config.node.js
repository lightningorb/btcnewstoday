// import adapter from '@sveltejs/adapter-auto';
// import adapter from '@sveltejs/adapter-static';
import adapter from '@sveltejs/adapter-node';
import preprocess from 'svelte-preprocess';


/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: preprocess({
        replace: [
                    [/process\.env\.NODE_ENV/g, JSON.stringify(process.env.NODE_ENV)],
                    [/process\.env\.IS_STATIC/g, JSON.stringify(process.env.IS_STATIC)],
                    [/process\.env\.PRE_RENDER/g, JSON.stringify(process.env.PRE_RENDER)],
                    [/process\.env\.SSR/g, JSON.stringify(process.env.SSR)],
                    [/process\.env\.CSR/g, JSON.stringify(process.env.CSR)]
                  ]
    }),
    kit: {
        adapter: adapter({
          ssr: {
            noExternal: ['@popperjs/core']
          }
        })
    }
};

export default config;
