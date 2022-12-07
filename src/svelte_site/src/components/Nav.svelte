<script lang="ts">
  import { preferences } from '$lib/store.js';
  import { Col, Container, Row } from 'sveltestrap';
</script>

<Container>
  <Row cols={1}>
    <Col>
      <nav class='main-nav'>
        <ul class="nav justify-content-center">
        <li class='nav-item'>
          <a class='nav-link' href="/" data-sveltekit-prefetch>Home</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/latest" data-sveltekit-prefetch>Latest</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/longform" data-sveltekit-prefetch>Longform</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/past" data-sveltekit-prefetch>Past</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/about" data-sveltekit-prefetch>About</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/events" data-sveltekit-prefetch>Events</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/podcasts" data-sveltekit-prefetch>Podcasts</a>
        </li>
        <li class='nav-item'>
          <a class='nav-link' href="/jobs" data-sveltekit-prefetch>Jobs</a>
        </li>
        {#if $preferences.access_token != ''}
          <li class='nav-item'>
            <a href="/dashboard" data-sveltekit-prefetch>Dashboard</a>
          </li>
        {/if}
        </ul>
      </nav>
    </Col>
  </Row>
</Container>
