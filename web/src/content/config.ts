import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  type: "content",
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
        z.object({
          name: z.string(),
          url: z.string().url(),
        }),
      )
      .default([]),
    heroImage: z.string().optional(),
  }),
});

export const collections = { blog };
