# THE WORLD — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/s8fr2hf/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/s8fr2hf/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A newspaper front page summing up the world news of Wednesday, 25 November 2026 — drawn entirely with Pillow primitives and DejaVu fonts, no photographs.

## The stories on the page

- **Lead — US intelligence:** The CIA and the Office of the Director of National Intelligence discovered a breach of the unclassified network they use to analyse open-source intelligence. Officials said no classified systems were affected, and the attacker is unknown. (New York Times, CNN, Reuters)
- **Middle East — Riyadh:** A Houthi drone struck Riyadh's tallest tower, home of the Public Investment Fund, wounding 11 people — the second hit on the tower in under a week. (Reuters)
- **Middle East — Defence:** Saudi Arabia has asked allies from America to Asia for help replenishing its missile defences. (Reuters)
- **Health — DR Congo:** The WHO evacuated staff from a hospital in Ituri, DR Congo, after three days sheltering from fierce fighting at the heart of the Ebola outbreak. (WHO)
- **Business — US economy:** US consumer confidence jumped to its highest in nearly two years, on optimism over jobs and the economy. (Reuters)
- **Tech — Huawei:** A US jury found Huawei guilty of stealing trade secrets, on 10 of 12 counts, but acquitted it of racketeering. (Reuters, BBC)

## How it works

`render.py` draws the 1024×1024 front page: masthead and dateline, a drawn server-room scene for the lead story, and five further stories with small drawn icons (tower, shield, medical cross, chart, chip). `main.py` (standard library only) copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and validates it (PNG, ≤ 1 MiB, 1024×1024).

## Run it

```sh
python3 main.py
```

Two runs produce byte-identical output.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=hwnj64tj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
