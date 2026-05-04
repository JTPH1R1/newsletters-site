import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://readomg.netlify.app',
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-light'
    }
  }
});
