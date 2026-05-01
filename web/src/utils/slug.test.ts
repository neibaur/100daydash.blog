import { describe, expect, it } from "vitest";

import { formatDaySlug } from "./slug";

describe("formatDaySlug", () => {
  it("pads day numbers to three digits", () => {
    expect(formatDaySlug(1, "us-ev-sales-trend")).toBe(
      "day-001-us-ev-sales-trend",
    );
  });
});
