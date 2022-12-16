/** @type {import('./$types').LayoutLoad} */

export function load() {
  return {
    sections: [
      // { slug: 'login', title: 'Log In', auth: false },
      { slug: 'add_article', title: 'Add Article', auth: true },
      { slug: 'add_podcast', title: 'Add Podcast', auth: true },
      { slug: 'add_event', title: 'Add Event', auth: true },
      { slug: 'add_job', title: 'Add Job', auth: true },
      { slug: 'article_drafts', title: 'View Article Drafts', auth: true },
      { slug: 'podcast_drafts', title: 'View Podcast Drafts', auth: true },
      { slug: 'archive', title: 'Archive', auth: false }
    ]
  };
}