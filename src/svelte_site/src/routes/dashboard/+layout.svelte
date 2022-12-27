<script>
	/** @type {import('./$types').LayoutData} */
	export let data;
	import { Col, Container, Row } from 'sveltestrap';
	import { preferences } from '$lib/store.js';
	import { logout } from '$lib/utils.js';
	import { base } from '$app/paths';
	import UserInfo from '../../components/UserInfo.svelte';
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faRightToBracket, faRightFromBracket } from '@fortawesome/free-solid-svg-icons/index.js';
	import { browser, dev } from '$app/environment';
</script>

{#if browser}
<Container>
	<Row cols={2}>
		<Col xs={2}>
			<div class="submenu">
				<br />
				{#each data.sections as section}
					{#if (section.auth == true && $preferences.access_token && section.roles.includes($preferences.role)) || section.auth == false}
						<a href={`${base}/dashboard/${section.slug}`}>
							{@html section.title}
							{#if section.icon}
								<Fa icon={section.icon} />
							{/if}
						</a>
						<br />
					{/if}
				{/each}
				<hr />
				{#if $preferences.access_token == ''}
					<a href={`${base}/dashboard/login`}>Log in <Fa icon={faRightToBracket} /></a>
				{:else}
					<a on:click={logout}>Log out <Fa icon={faRightFromBracket} /></a>
				{/if}
				<br />
			</div>
		</Col>
		<Col xs={10}>
			<slot />
		</Col>
	</Row>
</Container>
<br />
{/if}