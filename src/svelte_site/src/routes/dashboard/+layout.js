/** @type {import('./$types').LayoutLoad} */

export function load() {
  return {
    sections: [
      // { slug: 'login', title: 'Log In' },
      { slug: 'add_article', title: 'Add Article' },
      { slug: 'add_podcast', title: 'Add Podcast' },
      { slug: 'add_event', title: 'Add Event' },
      { slug: 'add_job', title: 'Add Job' }
    ]
  };
}