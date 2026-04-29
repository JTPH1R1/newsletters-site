import { defineCollection, z } from 'astro:content';

const newsletters = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    theme: z.string(),
    excerpt: z.string(),
    date: z.string(),
    dateSlug: z.string(),
    edition: z.number(),
    tags: z.array(z.string()).default([]),
    readTime: z.string().default('6 min read'),
    question: z.string(),
    coverImage: z.string().optional(),
    coverAlt: z.string().optional(),
    coverCredit: z.string().optional(),
    numbers: z.array(z.object({
      label: z.string(),
      value: z.string(),
      meaning: z.string()
    })).default([])
  })
});

export const collections = { newsletters };
