[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/andikaprp/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/andikaprp/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# One Page — The World on Wednesday 25 November 2026

Entry for the make.fun competition **news-image-20261125**: sum up one
day's world news in a single image.
[Bounty: Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)

## The page

A cream broadsheet front page for Wednesday 25 November 2026: a giant
serif date, the day in UTC, a six-figure stat band, 13 illustrated
story cards (US tariffs on 14 partners as the lead, two tankers mined
in Hormuz, Russia's strike on Ukraine's grid), 26 one-line briefs, a
pin map and a DATE CHECK box naming the earlier-day stories left out
on purpose. 39 stories, 7 regions, every item verified against
Tier-1 wire or official sources with its event time on the day.

## How it runs

- `main.py` — the entrypoint. Standard library only. It copies the
  shipped `entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`,
  default `/output`). The copy is byte-identical on every run.
- `entry.png` — the finished page (1024 x 1024, under 1 MiB).
- `render.py`, `panels.py`, `worldmap.py` — the renderer that drew
  the page from the data file (13 bespoke panels, no shared template).
- `data.json` — the day's verified census as data.

## License

MIT — see `LICENSE`.
