# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Kodoku05/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Kodoku05/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The World Today — 21 November 2026: a program that sums up the world news
of Saturday 21 November 2026 as a one-page newspaper front page (a 1024×1024
PNG). Lead story: Poland reports a Russian missile strike on its soil during
Moscow's barrage on Ukraine; plus the first-ever Trump–Xi–Putin trilateral in
Shenzhen, the ICJ's genocide ruling against Myanmar, Bitcoin sinking below
$59,000, COP31 running into overtime, and Cyclone Akvan fading over Odisha.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`). Node 22,
standard library only. Deterministic: repeated runs produce identical bytes.
`draw_poster.py` (Python + Pillow) regenerates the poster from the news data
in `news.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p2xp6s2q&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
