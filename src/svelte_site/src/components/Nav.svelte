<script lang="ts">
  import { page } from '$app/stores';
  import { preferences } from '$lib/store.js';
  import { Col, Container, Row } from 'sveltestrap';
  import {base} from '$app/paths';
  import { Icon } from 'sveltestrap';
</script>

<Container>
  <Row cols={1}>
    <Col>
      <nav class='main-nav'>
        <ul class="nav justify-content-center">
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/`} data-sveltekit-prefetch>Home</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/latest`} data-sveltekit-prefetch>Latest</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/longform`} data-sveltekit-prefetch>Longform</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/past`} data-sveltekit-prefetch>Past</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/about`} data-sveltekit-prefetch>About</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/events`} data-sveltekit-prefetch>Events</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/podcasts`} data-sveltekit-prefetch>Podcasts</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/jobs`} data-sveltekit-prefetch>Jobs</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href={`${base}/prefs`} data-sveltekit-prefetch>Prefs</a>
        </li>
        {#if $preferences.access_token != ''}
          <li class='nav-item'>
            <a href={`${base}/dashboard`} data-sveltekit-prefetch>Dashboard</a>
          </li>
        {/if}
        <li>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='{base}/search'><Icon name="search"/></a>
        </li>
        </ul>
      </nav>
    </Col>
  </Row>
</Container>
