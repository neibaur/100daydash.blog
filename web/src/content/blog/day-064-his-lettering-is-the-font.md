---
title: "Day 64 - July 4, 2026: His Lettering Is the Font"
description: "A Day 64 reflection on turning Kai's Boo-Boo Story drawings into game assets, preserving hand-drawn identity, using manual crops with automated cleanup, and watching governed agents refuse to fabricate missing inputs."
pubDate: "2026-07-04"
day: 64
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story art-processing implementation notes"
  - "Boo-Boo Story prototype notes"
  - "Boo-Boo Story ADR 0006 notes"
  - "Boo-Boo Story missing-asset handoff notes"
  - "Boo-Boo Story validation notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - prototyping
  - game-design
  - image-processing
  - product-design
  - developer-experience
---

Day 64 was the day Boo-Boo Story stopped borrowing a style and started using
its source material.

Kai had drawn two important pieces:

- a Boo-Boo Story title screen
- a hand-drawn world map

Those drawings changed the project.

Before that, Boo-Boo Story had been a set of small playable questions. Which
mode feels right? Map? Walk? Story? Quest? How much movement matters? How
much discovery matters?

Yesterday made the visual question sharper.

The point is not to make a polished game that vaguely resembles Kai's
drawings. The point is to build around the drawings themselves.

His lettering is the font.

That is the sentence that kept pulling the work back into focus.

The pencil texture, uneven lines, bubble lettering, character shapes, and
small asymmetries are not rough drafts of a cleaner asset library. They are
the visual identity of the thing.

The job of the code is to help those drawings become playable without quietly
replacing them.

## The Drawings Became The Source Of Truth

The title-screen scan and world-map scan needed practical work before they
could be used as game assets.

They had to be rotated. They had to be cleaned. Pencil marks needed to be
separated from paper without turning into harsh black-and-white clip art.
Pieces of the drawings needed transparent backgrounds. Some assets needed a
light fill. Some needed a horizontal ground line removed.

That could have become the moment to recreate everything as SVGs.

It would have been tempting.

SVGs are neat. Fonts are consistent. Polished assets are easier to align.
Programmer-created shapes feel controllable.

But that would have solved the wrong problem.

The drawings are not a prompt for a different art style. They are the art
style.

A cleaner imitation would have made the game look more professional in the
least interesting way. It also would have made the project less Kai's.

So the product decision was to preserve the scanned artwork and make the game
adapt to it.

That sounds simple until the first extraction goes wrong.

## The AI Found The Wrong Boo-Boo

The funniest failure of the day was also one of the most useful.

Claude initially tried to identify and extract Boo-Boo from the full
title-screen scan.

It confidently picked the wrong thing.

Instead of isolating the actual character, it effectively treated part of the
drawing that looked more like a doorway or shop shape as the hero.

That mistake was funny because it was so confident. It was useful because it
made the boundary obvious.

The real Boo-Boo has a large round head, a very short stick-like body, bulbous
hands and feet, dark vertical-line eyes, a small dot mouth, and an
upward/right-looking pose. In the original drawing, he is standing on a
straight horizontal ground line.

To a human looking at Kai's drawing, that is the character.

To an automated process looking at a noisy scan with hand-drawn forms,
semantic certainty is fragile.

The fix was not to build a better detector.

I provided a manual crop of the actual Boo-Boo.

That tiny human input removed the ambiguity immediately.

The lesson was not "never automate image work." The lesson was more precise:

- automate repeatable cleanup
- keep semantic identification manual when the drawing is ambiguous
- do not build speculative auto-detection machinery before the pain is real

That fits the broader pattern from recent days.

Infrastructure should wait for felt pain. And when it arrives, the tool
should be the size of the pain, not the size of the engineer's imagination.

## Manual Crop, Automated Cleanup

Once the correct Boo-Boo crop existed, the next question was how to make the
character usable in a game without redesigning him.

The original crop had two problems.

First, the character interior was transparent. That worked as extracted ink,
but it did not read as strongly as a game sprite.

Second, the crop included the horizontal line Boo-Boo was standing on. When
the character moved, the line moved too. Suddenly Boo-Boo was carrying a
little floor around with him.

That was funny for about two seconds.

Then it became a useful asset-processing requirement.

The prototype was revised so Boo-Boo could keep the original pencil facial
details while gaining a marker-like yellow fill:

```text
#F6C445
```

The horizontal ground line was removed.

Then a temporary three-frame animation was created:

- stand
- walk frame 1
- walk frame 2

The walk frames used small programmatic shears to move the legs and
counter-swing the arms. The frames shared the same dimensions so the sprite
would not jitter. When Boo-Boo moves, the prototype cycles through the walk
frames. When he stops, it returns to the standing frame.

That is useful.

It is also a placeholder.

The real long-term answer is probably for Kai to draw two or three walk poses
himself. The programmatic walk cycle is a bridge, not a replacement for the
artist.

That distinction matters because code can slowly become too helpful.

It can smooth the lines. It can generate the missing frames. It can start
"improving" the art until the original author is only present as an
inspiration.

That is not the direction I want.

The tooling should support Kai's art, not quietly supersede it.

## The Prototype Became Personal

The updated Boo-Boo Quest prototype felt different once Kai's actual work was
inside it.

The title screen used his hand-drawn "Boo-Boo Story the GAme" lettering. The
game used the corrected Boo-Boo character. The map view incorporated his
world-map concept. The prototype added an `art by Kai` credit.

None of that makes the game finished.

But it makes the prototype more honest.

It is no longer only a parent and some agents testing generic adventure-game
mechanics. It is beginning to ask whether Kai's own drawings can become the
center of the experience.

There was also a delightful design coincidence in the world map.

Kai marked unexplored places with `???`.

The existing Zelda-style exploration prototype already had question marks and
fog-of-war-like ideas for unknown areas.

That does not prove the mechanic is settled. A coincidence is not a product
requirement.

But it is product evidence.

The creator's own map drawing independently reflected one of the prototype's
exploration ideas. That is worth paying attention to.

Good prototype work is full of moments like that. Not proof. Signal.

## One Small Tool Earned Its Place

Earlier in the Boo-Boo Story work, I had been cautious about creating an image
pipeline.

That caution was right.

One scan does not justify a system. One cleanup task does not justify a
framework. One interesting asset does not justify an asset-processing
platform.

But yesterday the same scan operations repeated enough times that a small
script finally earned its place:

```text
scripts/process_scan.py
```

The important part is what the script did not become.

It stayed intentionally small, around 113 lines. It used Pillow, NumPy,
SciPy, and `argparse`. It handled the repeatable operations that had actually
caused pain:

- image or scanned-PDF input
- rotation
- soft-threshold conversion of pencil marks to alpha
- preservation of light pencil texture
- recoloring extracted ink to pencil gray near `#3A3A3A`
- optional interior flood-fill with a hex color
- optional removal of thin horizontal strokes in a specified row band

The scan settings that emerged were concrete enough to remember without
turning the post into an image-processing tutorial:

- paper around `246`
- depth around `70`
- gamma `0.5`
- morphology around a `7x1` structure for thin-line removal

That is the right scale of detail.

The broader point is the governance one.

Deferred infrastructure finally crossed the felt-pain threshold. But what
entered the repository was a focused CLI script, not a generalized art
pipeline, automatic crop detector, sprite tooling suite, configuration
system, or image CDN.

The shape of the tool matched the shape of the repeated work.

That is the part I want to keep practicing.

## The ADR Captured The Boundary

The implementation also added an ADR for the art pipeline.

There was a small repository-grounding moment there too.

The requested ADR number had originally been `0003`, but that number already
existed. Fable followed the repository's actual sequence instead of the stale
prompt and created:

```text
docs/adr/0006-kai-art-pipeline.md
```

That sounds like bookkeeping.

It is more than that.

A good agent should read the repository and let existing facts override a
literal instruction when the literal instruction is stale.

The ADR recorded the important product and implementation boundaries:

- use Kai's actual scanned artwork instead of recreating the style
- preserve pencil texture through soft-threshold extraction
- keep character and element cropping manual
- avoid auto-detection until there is real evidence it is needed
- treat the sheared walk cycle as a placeholder
- credit artwork as `art by Kai`, using first name only

That ADR matters because the tempting future failure is obvious.

As the prototype grows, a new prompt could ask an agent to "clean up" the art,
generate more polished sprites, or create missing poses.

Without a recorded decision, that might sound reasonable.

With the ADR, the repository has a clearer answer: the creator stays
authoritative over meaning and visual identity. The tooling handles
repeatable translation work around the art.

## The Missing Assets Were The Strongest Test

The most important governance moment was not the sprite fill or the Python
script.

It was missing input files.

The first implementation prompt listed nine expected image assets. Fable
found only the three walk-cycle sprite files and the demo HTML in the staging
folder.

Six expected assets were absent.

That is exactly where an agent workflow can go soft.

It could draw substitutes. It could create placeholder images. It could infer
what the missing assets were supposed to be. It could pretend the files
existed and wire paths that would fail later.

Instead, it searched the repository, reported exactly which files were
missing, and stopped that portion of the work.

Later, the missing inputs were supplied and the agent was re-prompted.

Five additional assets were added:

- `boo-boo-sprite.png`
- `title-lettering.png`
- `title-screen.png`
- `world-map.png`
- `world-map-transparent.png`

A separate `boo-boo-yellow.png` never arrived.

Fable did not fabricate it.

It observed that `boo-boo-stand.png` already served as the un-sheared yellow
base pose and left the redundant file absent.

That is the most concrete governance win of the day.

Recent posts have talked a lot about `AGENTS.md`, source grounding,
protected-path discipline, repo facts beating prompt memory, and claims as
pointers rather than evidence.

This was those ideas under pressure.

The agent encountered incomplete inputs and effectively said: these files do
not exist, so I will not invent them.

That does not prove the system is hallucination-proof. It does not mean every
future agent will behave correctly. It is one successful observed behavior
under an incomplete-input condition.

That is still valuable evidence.

Governance is easiest to dismiss when everything goes smoothly. Its value
shows up when the prompt asks for a world that the filesystem does not
contain.

## Repository Facts Beat Prompt Assumptions

There were several smaller examples of the same behavior.

The prototype was placed at:

```text
packages/site/public/play/quest-kai/index.html
```

That serves it at `/play/quest-kai/`, matching the existing
directory-with-index convention instead of following a stale bare-file
suggestion like `quest-kai.html`.

The existing Boo-Boo Quest demo was preserved.

The `/play` index listed `Boo-Boo Quest (with Kai's real art!)` first.

The art assets lived under:

```text
packages/site/src/assets/kai/
```

The ADR used `0006` rather than colliding with `0003`.

`temp/` was added to `.gitignore` and `.prettierignore` because it was acting
as a staging inbox and the raw demo there was interfering with validation.

The demo was copied byte-for-byte and verified with `cmp`.

The site still built successfully with six pages. `pnpm validate` passed. The
relevant generated pages retained `noindex`, and the existing
`X-Robots-Tag: noindex` header continued to cover the site.

Those details should not turn the post into a changelog.

The pattern is the point.

A good agent should not mechanically obey a prompt when the repository says
the prompt is stale. It should adapt to local conventions, preserve existing
work, avoid fabricating missing inputs, and validate the result.

Yesterday had several examples of that behavior in one small game-art loop.

## Why The Day Mattered

Day 64 mattered because it made the Boo-Boo Story direction more concrete
without making it less Kai's.

The project did not become more interesting because the game looked more
polished.

It became more interesting because the real drawings became authoritative.

That changed the work.

The goal is not to imitate a child's drawing style with cleaner assets. The
goal is to preserve the creator's hand while using code to handle the boring
translation work: rotation, thresholding, recoloring, fill, line removal,
file placement, route conventions, and validation.

The AI mistaking a doorway for Boo-Boo was the perfect little warning.

Meaning is not always obvious to automation.

A human-provided crop can be better than a speculative detector. A focused
113-line script can be better than an art pipeline. A missing file report can
be better than a generated placeholder. A repository-grounded ADR number can
be better than a literal prompt.

That is the kind of agentic engineering I want.

Not maximal automation.

Appropriate automation.

Kai remains authoritative over the character, the map, the lettering, and the
visual identity. The tooling earns its keep by helping those things survive
the trip from paper to playable prototype.

## Outcome

Day 64 moved Boo-Boo Story from generic prototype aesthetics toward using
Kai's real scanned artwork as the source of visual truth.

Kai had drawn a Boo-Boo Story title screen and a hand-drawn world map. The
work focused on rotating, cleaning, extracting, and processing those scans so
they could become game assets without replacing their pencil texture,
uneven lines, bubble lettering, and original character shapes.

The key product decision was to preserve the drawings rather than recreate
them as polished SVGs, AI-generated approximations, or a vaguely similar
font. The title lettering itself became part of the identity. The game should
adapt to Kai's art, not smooth it away.

Claude initially tried to extract Boo-Boo from the full title-screen scan and
identified the wrong object, effectively mistaking a doorway or shop-like
shape for the hero. I corrected that by providing a manual crop of the actual
Boo-Boo: a large round head, short stick-like body, bulbous hands and feet,
vertical-line eyes, dot mouth, upward/right-looking pose, and original ground
line.

That failure clarified the image-processing boundary. Repeatable cleanup can
be automated, but semantic identification and cropping should remain manual
when the source drawing is ambiguous. The project does not need speculative
auto-detection or segmentation machinery yet.

The corrected Boo-Boo crop was turned into a more game-like sprite while
preserving the original pencil details. Boo-Boo received a marker-like yellow
fill of `#F6C445`, the floating ground line was removed, and a placeholder
three-frame animation was created: stand, walk frame 1, and walk frame 2. The
walk frames used small programmatic shears, shared dimensions, and idle versus
moving animation behavior. This is explicitly temporary until Kai draws real
walk poses.

The updated Boo-Boo Quest prototype used Kai's hand-drawn title lettering,
the corrected Boo-Boo sprite, the hand-drawn world-map concept, and an
`art by Kai` credit. Kai's map also used `???` for unexplored places, which
matched the existing exploration prototype's question-mark and fog-of-war
ideas closely enough to count as useful product signal, not final proof.

The repeated scan work finally justified a small image-processing utility:
`scripts/process_scan.py`. It stayed intentionally focused at about 113
lines, using Pillow, NumPy, SciPy, and `argparse` for image or scanned-PDF
input, rotation, soft-threshold pencil extraction, pencil-gray recoloring near
`#3A3A3A`, optional hex flood fill, and optional thin-horizontal-line removal
using a morphology operation around `7x1`. The approximate scan settings were
paper `246`, depth `70`, and gamma `0.5`.

The implementation added `docs/adr/0006-kai-art-pipeline.md` after detecting
that the originally requested ADR number `0003` already existed. The ADR
captured the decisions to use Kai's scanned artwork, preserve pencil texture,
keep cropping manual, avoid auto-detection, treat the sheared walk cycle as a
placeholder, and credit artwork as `art by Kai`.

The strongest governance moment came from missing assets. The first
implementation prompt listed nine expected image files, but Fable found only
the three walk-cycle sprite files and the demo HTML in the staging folder. It
searched the repository, reported the six missing files, and stopped that
portion of the work instead of fabricating placeholders. After the missing
files were supplied, it added `boo-boo-sprite.png`, `title-lettering.png`,
`title-screen.png`, `world-map.png`, and `world-map-transparent.png`. A
separate `boo-boo-yellow.png` never arrived, and the agent left it absent
because `boo-boo-stand.png` already served as the yellow base pose.

Several repository-grounded implementation choices also held. The new
prototype followed the existing `/play/*/index.html` convention at
`packages/site/public/play/quest-kai/index.html`, preserved the existing demo,
listed `Boo-Boo Quest (with Kai's real art!)` first on the play index, placed
art assets under `packages/site/src/assets/kai/`, ignored the staging `temp/`
folder, copied the demo byte-for-byte, preserved `noindex`, and passed
validation.

## Definition Of Done

Day 64 reached the Boo-Boo Story real-art prototype checkpoint:

- confirmed Day 64 follows Day 63 for July 4, 2026
- centered Kai's title-screen and world-map drawings as source material
- chose to preserve the scanned artwork rather than recreate the style
- treated the hand-drawn lettering as part of the product identity
- preserved pencil texture, uneven lines, bubble lettering, and character
  shapes as intentional visual language
- observed the failed automatic Boo-Boo extraction
- identified that the AI selected a doorway or shop-like shape instead of the
  character
- corrected the workflow with a manual crop of the real Boo-Boo
- documented the real Boo-Boo features used for identification
- drew the boundary between manual semantic cropping and automated cleanup
- avoided speculative auto-detection or segmentation infrastructure
- filled Boo-Boo with marker-like yellow `#F6C445`
- preserved the original dark pencil facial details
- removed the horizontal ground line from the moving sprite
- created stand, walk frame 1, and walk frame 2 placeholders
- used small programmatic shears for temporary motion
- kept animation frame dimensions stable to avoid jitter
- cycled walk frames only while moving
- returned to the standing frame while idle
- treated the walk cycle as temporary until Kai draws real poses
- added Kai's real title lettering to the prototype
- incorporated the corrected Boo-Boo character
- incorporated the hand-drawn world-map concept
- added the `art by Kai` credit
- noticed the map's `???` unexplored-place marker as product signal
- allowed repeated scan pain to justify a small image-processing CLI
- kept `scripts/process_scan.py` focused instead of building a broad pipeline
- supported rotation, soft-threshold extraction, pencil recoloring, optional
  fill, and optional line removal
- used scan settings around paper `246`, depth `70`, and gamma `0.5`
- used thin-line morphology around a `7x1` structure
- captured the art-pipeline decision in ADR `0006`
- corrected the stale requested ADR number instead of colliding with `0003`
- recorded manual cropping as a deliberate decision
- recorded the sheared animation as a placeholder
- recorded first-name-only artwork credit
- found missing prompted assets instead of inventing them
- stopped the incomplete-input portion of the implementation
- later added the supplied title, map, transparent map, and sprite assets
- left the absent redundant `boo-boo-yellow.png` unfabricated
- reused `boo-boo-stand.png` as the yellow base pose
- followed the repository's directory-with-index play route convention
- preserved the existing Boo-Boo Quest demo
- placed Kai art assets under the existing project asset conventions
- ignored `temp/` as staging inbox noise
- verified the demo copy byte-for-byte
- preserved `noindex` behavior
- passed site validation
- preserved the core lesson: the creator stays authoritative over visual
  identity, and tooling handles repeatable translation work
