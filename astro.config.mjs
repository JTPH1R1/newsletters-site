import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://readomg.netlify.app',
  output: 'static',
  integrations: [
    sitemap()
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light'
    }
  }
});
