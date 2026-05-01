export function formatDaySlug(day: number, slug: string): string {
  return `day-${day.toString().padStart(3, "0")}-${slug}`;
}
