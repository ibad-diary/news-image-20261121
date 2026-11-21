# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ibad-diary/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ibad-diary/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up Saturday, 21 November 2026 in a single image: 37 stories (3 illustrated leads, 10 illustrated features, 24 one-line briefs), a numbers strip, and a date-check footer that explicitly excludes stories first reported on Friday 20 November (Cyclone Akvan's landfall, the Trump–Xi–Putin Shenzhen summit, Anthropic's $83 IPO debut, the ICJ Myanmar verdict, GTA VI launch). Every picture is drawn in code.

## Run it

```sh
python3 generate_image.py   # renders entry.png (1024x1024, <= 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies it to out/
```

Run `main.py` twice and diff the outputs: they must be byte-identical.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s67gjd7a&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
