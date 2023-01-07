<script>
	import { preferences } from '$lib/store.js';
	import { get } from 'svelte/store';
	import { Form, FormGroup, FormText, Label, Input } from 'sveltestrap';

	$: show_images = get(preferences).show_images;
	$: dark = get(preferences).theme_name === 'dark';
	$: show_bounties = get(preferences).show_bounties === true;

	function handleClick(event) {
		let p = get(preferences);
		show_images = !show_images;
		p.show_images = show_images;
		preferences.set(p);
	}

	function handleBountyClick(event) {
		let p = get(preferences);
		show_bounties = !show_bounties;
		p.show_bounties = show_bounties;
		preferences.set(p);
	}

	function handleDarkClick(event) {
		let p = get(preferences);
		dark = !dark;
		p.theme_name = dark ? 'dark' : 'light';
		window.location.reload();
		preferences.set(p);
	}
</script>

<h1>Site Prefs</h1>
<br />
<Input type="switch" checked={show_images} on:change={handleClick} /> <span>Show Images</span><br />
<hr/>
<Input type="switch" checked={show_bounties} on:change={handleBountyClick} /> <span>Show Bounties</span><br />
<hr/>
<Input type="switch" checked={dark} on:change={handleDarkClick} /> <span>Dark Mode</span><br />
<br />
