# Saturday 21 November 2026: 37 dated stories, 10 regions — Iran hits Bahrain bases, deep Peru quake, COP31 overtime

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261121)
[![prize $100](https://img.shields.io/badge/prize-%24100-green)](https://make.fun/bounty/news-image-20261121)
[![deadline 23 Nov 2026 00:00 UTC](https://img.shields.io/badge/deadline-23%20Nov%202026%2000%3A00%20UTC-orange)](https://make.fun/bounty/news-image-20261121)

Bounty: [make.fun — Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121)

One front page, 1024×1024, that sums up the world's news of **Saturday 21
November 2026**: 37 stories from 10 regions, every one dated that Saturday
and backed by at least two outlets.

## The day in one line

COP31 drifts into overtime with no deal in sight; Iran claims missile-and-
drone strikes on two US bases in Bahrain while Bahrain reports a civilian
plant fire and no dead; a deep M6.7 quake shakes central Peru.

## What is on the page

- **Masthead** — "THE WORLD IN ONE DAY", Saturday 21 November 2026, updated
  22 Nov 2026 03:30 UTC.
- **Number strip** — six figures from the day, including "16 CREW SAFE,
  SPARTA II".
- **3 leads** — COP31 overtime (Antalya), Iran's Bahrain claim (Manama),
  Peru M6.7 (Junín). Each carries a hand-drawn icon, a city line, and a
  status tag.
- **10 features** — Sparta II ablaze in the Gulf of Finland (all 16 crew
  safe), 'Chapo Isidro' captured in Sinaloa, the Kryvyi Rih triple-tap
  strike, the US AI stock sell-off, the Java candy-factory fire, the
  EU–Indonesia trade deal, the Nigeria boat capsize, Bolsonaro in intensive
  care, Denmark's assassination-plot charge, and the Basra power-plant fire.
- **World map, numbered 1–37** — Washington is a triangle; Kyiv, Kryvyi
  Rih, Copenhagen and the Gulf of Finland are kept apart on purpose, and
  close dots are spaced for legibility.
- **24 numbered briefs** — the rest of the day, three columns.
- **DATE CHECK box** — the dating rule, in print on the page (see below).
- **Tags** — every illustrated card is marked OFFICIAL, CLAIM or REPORTED.
  Iran's Bahrain strike and Denmark's plot charge are CLAIMs: the claim is
  reported, the fact is not asserted. The EU–Indonesia deal and the
  Azerbaijan state visit are OFFICIAL. Everything else is REPORTED.

## Date rule

Every story is dated Saturday 21 November 2026. Friday-night events are in
only where the announcement, bulletin or toll update came on Saturday:
'Chapo Isidro' was arrested Friday night and announced Saturday morning;
the Peru quake struck 19:09 Friday local, which is 00:09 Saturday UTC;
the Kryvyi Rih toll was updated Saturday morning; the Nigeria toll of 24
was confirmed Saturday; Bolsonaro was taken to hospital Friday, with the
ICU bulletin Saturday; Denmark's plot charge, the Rikers plan and the
Harden game were announced Friday and reported Saturday.

**COUNTS DIFFER:** tolls moved as reports came in during the day — Kryvyi
Rih 58–60 hurt, Basra 30–35 hurt, Nigeria 23–24 dead. The figures on the
page are those reported on 21 November.

## Regions (37 stories)

| Region | Stories |
| --- | --- |
| North America | 4 |
| South America | 4 |
| Middle East | 4 |
| East Asia | 3 |
| Southeast Asia | 3 |
| South Asia | 4 |
| Europe | 6 |
| Africa | 4 |
| Oceania | 3 |
| Central Asia & Caucasus | 2 |

## Stories and outlets

1. COP31 drifts into overtime — Reuters, AP
2. Iran says it hit two US bases in Bahrain — Xinhua, Reuters
3. Deep M6.7 quake shakes central Peru — USGS, AP
4. Sparta II ablaze in the Gulf of Finland — Reuters, CNN
5. 'Chapo Isidro' captured in Sinaloa raid — Reuters, CNN
6. Missiles hit Zelenskyy's home city — AP, CNN
7. AI sell-off drags US stocks into correction — OneTurn, Juba Global
8. Candy factory fire: 3 dead, 36 missing — Reuters, AP
9. EU and Indonesia sign landmark trade deal — European Commission, AP
10. Boat capsize kills 24 on way to a funeral — Reuters, AP
11. Bolsonaro in intensive care in Brasília — Reuters, CNN
12. Denmark says Russia plotted to kill rapper — WSJ, Fox News
13. Fire at Basra power plant kills 4 — Reuters, Al Jazeera
14. Harden scores 51, passes Kobe Bryant — AP, theScore
15. Mamdani vows to shut Rikers by 2032 — AP, CNN
16. Bug mosquitoes cut dengue 69% in Brazil — AP, TechTimes
17. CONMEBOL backs Infantino for FIFA top job — AFP, Reuters
18. Three Houthi missiles at Riyadh intercepted — Reuters, AFP
19. Israeli strikes kill six in Gaza — WAFA, Juba Global
20. 47,000 sign against Japan nuclear subs — Dimsum Daily, EIN Presswire
21. Urrutia wins Macau TCR Race 1 — EIN Presswire, FIA TCR
22. Trump, Xi back human control of military AI — Dimsum Daily, EIN Presswire
23. Azerbaijan's Aliyev gets Hanoi welcome — EIN Presswire, Azerbaijan Presidency
24. Illicit liquor kills 11 in Manipur — Al Jazeera, Archipelago Expat
25. Bangladesh marks Armed Forces Day — TBS News, UNB
26. Bangladesh pitches tri-nation series — Cricbuzz, CricTracker
27. Japan to fire missiles on Indian ranges — Asia Daily, QNC News
28. French police guilty over Zecler beating — Al Jazeera, France 24
29. Zelenskyy: Putin is 'a killer' — CNN, TBS News
30. ANC fights to hold South Africa's big cities — BBC, Afrikactus
31. Ireland edge South Africa 20–17 in Dublin — BBC, The Guardian
32. Joburg turns on Level 2 water curbs — SAnews, EWN
33. Australia beat New Zealand 3–1 in Auckland — All Football, EIN Presswire
34. Aid rushed to Bougainville as El Niño looms — PNG Post-Courier, EIN Presswire
35. India post record 720 in Wellington Test — EIN Presswire, Times of India
36. Russia NATO demands alarm Caucasus, C. Asia — RFE/RL, Wisevoter
37. Middle Corridor: 30M tonnes by 2029 — Caucasus Business Journal, Euronews

## How it is built

- `stories.json` — the 37 stories: number, region, kind, city, coordinates,
  title, dek, outlets, status tag, icon.
- `generate_image.py` — draws the page with Pillow (build-time only). All
  icons are drawn in code; there are no photo assets and no network calls.
- `main.py` — renders `entry.png`, copies it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, and verifies PNG magic, size (≤ 1 MiB)
  and dimensions (1024×1024).

## Run

```sh
python3 main.py
```

Runs twice and writes byte-identical files: fixed fonts, fixed strings, no
clock, no randomness. Requires Python 3.13 and Pillow.

## License

MIT — see `LICENSE`.
