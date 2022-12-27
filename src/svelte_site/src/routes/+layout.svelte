<script>
	import { Styles } from 'sveltestrap';
	import Nav from '../components/Nav.svelte';
	import Banner from '../components/Banner.svelte';
	import Footer from '../components/Footer.svelte';
	import { preferences } from '$lib/store.js';
	import { base } from '$app/paths';
	import { browser, dev } from '$app/environment';
	import { save_user_info } from '$lib/utils.js';
	import { Col, Container, Row } from 'sveltestrap';
	import { get } from 'svelte/store';
	import '$lib/interceptors.js';

	let p = get(preferences);
	p.podcast = '';
	preferences.set(p);
	let theme_name = p.theme_name || 'light';

	// save_user_info();

	if (dev == false && base === '' && browser == true && p.access_token == '') {
		(function (h, o, t, j, a, r) {
			h.hj =
				h.hj ||
				function () {
					(h.hj.q = h.hj.q || []).push(arguments);
				};
			h._hjSettings = { hjid: 3292513, hjsv: 6 };
			a = o.getElementsByTagName('head')[0];
			r = o.createElement('script');
			r.async = 1;
			r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
			a.appendChild(r);
		})(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');
	}
</script>

<svelte:head>
	<link rel="stylesheet" href="{base}/style-{theme_name}.css" />
</svelte:head>
<Styles />
<Banner />
<Nav />
<Container>
	<Row cols={1}>
		<Col><slot /></Col>
	</Row>
</Container>
<Nav />
<Footer />
