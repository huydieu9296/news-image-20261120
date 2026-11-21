[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/huydieu9296/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/huydieu9296/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

One image that tells the story of Friday 20 November 2026: six
stories, each verified against reports from the day itself.

| # | Story |
|---|---|
| 1 | Trump, Xi and Putin sign a "Declaration Towards Peace" after their Shenzhen summit |
| 2 | A Houthi missile damages Riyadh's tallest tower, the Saudi wealth fund's HQ |
| 3 | Cyclone Akvan makes landfall on India's east coast; 300,000 evacuated |
| 4 | Anthropic soars on its Nasdaq debut — the biggest IPO ever |
| 5 | Kushner says Russia is "comfortable" with NATO-style guarantees for Ukraine |
| 6 | Gazans return home as Israel's rare tank raid in central Gaza ends |

The page is a classic broadsheet: a navy masthead with the date, a
red rule, and six cards in two columns. Every card has a coloured
spine, a small line glyph, a kicker, a headline, a two-line deck and
a key fact. Headlines shrink until they fit two lines; nothing is
ever drawn outside its card.

## Sources

- Story 1 — Japan Times, "China, U.S. and Russia issue 'peace
  declaration' after unprecedented summit", 19 Nov 2026; Aju Press,
  "Three powers pledge peace, leave doubts", 20 Nov 2026.
- Story 2 — Reuters via The Straits Times / SCMP / Al Jazeera,
  "Riyadh's tallest skyscraper hit in Houthi strike on Saudi wealth
  fund HQ", 19–20 Nov 2026.
- Story 3 — The Hindu, "Cyclone 'Akvan' updates: Three lakh
  evacuated, 423 rescue teams deployed", 20 Nov 2026; India
  Meteorological Department bulletin, 19 Nov 2026. Landfall near
  Gopalpur was in the morning (about 7:30–11:20 am), with winds of
  70–80 km/h gusting to 90 km/h — not at noon, and not 110 km/h.
- Story 4 — The Wall Street Journal, "Anthropic's Mega IPO Lives Up
  to Wall Street Hype but Fails to Revive AI Trade", 20 Nov 2026;
  Nikkei Asia, "Anthropic opens up 34% in trading debut after
  record IPO", 20 Nov 2026.
- Story 5 — Associated Press via Arab News, "Kushner says he
  believes Russia is 'comfortable' with NATO-like security
  guarantees for Ukraine", 19 Nov 2026; Al Jazeera, 19 Nov 2026.
- Story 6 — Free Malaysia Today / AFP, "Gazans return after Israel
  army ends rare ground operation", 20 Nov 2026; Reuters, "Israel
  says it concludes Gaza tank raid", 19 Nov 2026.

## How to run it

```sh
python3 draw_news.py   # renders entry.png, 1024x1024, under 1 MiB
python3 main.py        # checks the file and copies it to $MAKEFUN_OUTPUT_DIR
```

`draw_news.py` needs Pillow and the DejaVu fonts that ship with the
system. `main.py` needs nothing but the standard library. The output
is byte-for-byte deterministic: the same fonts, the same geometry, no
randomness, no clock, no network.
