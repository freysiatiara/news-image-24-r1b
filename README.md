# The World in One Day — Tuesday 24 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261124-blue)](https://make.fun/bounty/news-image-20261124)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A single-image front page summing up 24 November 2026's world news — 31
stories across 7 regions, drawn from wire reports of 22–24 November 2026.

## What's inside

- `draw.py` — Pillow generator that renders `entry.png` (1024×1024, ≤1 MiB,
  deterministic: two runs are byte-identical).
- `main.py` — stdlib-only entry point. Regenerates `entry.png` and copies it
  to `/output/entry.png`, as the grader expects.
- `entry.png` — the finished front page.

## Headlines

- **Ukraine's drones sink a Russian warship — in Libya.** Seven sea drones
  sank the corvette *Merkury* at Benghazi; Zelenskyy confirmed it on Monday.
- **The AI rout deepens — then Nvidia bounces.** S&P 500 −3.7%, Nasdaq
  −5.3%; KOSPI −5.8% on Monday; Nvidia +8.7%.
- **24 dead in the Banten candy-factory fire**, with ~30 still missing.
- COP31 ends with no fossil-fuel deal; India–Nepal sign 8 MoUs; plus 26
  more stories, a dotted world map with 12 pins, and a date-check box.

## Reproduce

```sh
python3 draw.py        # writes entry.png
python3 main.py        # writes entry.png and /output/entry.png
```

Every fact on the page was checked against wire reports (AP, Reuters, BBC,
Bloomberg, ANI) dated 22–24 November 2026. See the DATE CHECK box on the
page itself for the dating of each lead story.

Built for the [make.fun news-image-20261124 bounty](https://make.fun/bounty/news-image-20261124).
