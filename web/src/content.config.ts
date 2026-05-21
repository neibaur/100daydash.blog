import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/blog",
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    day: z.number().int().min(0).max(100),
    dashboardSlug: z.string(),
    status: z.enum(["draft", "published", "archived"]).default("draft"),
    tags: z.array(z.string()).default([]),
    dataSources: z
      .array(
        z.union([
          z.string(),
          z.object({
            name: z.string(),
            url: z.url(),
          }),
        ]),
      )
      .default([]),
    heroImage: z.string().optional(),
  }),
});

export const collections = { blog };
