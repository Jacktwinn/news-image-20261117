# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Jacktwinn/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Jacktwinn/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page that sums up Tuesday 17 November 2026 in one image: the Kerch Bridge partially collapsed after a Ukrainian strike, Trump in Manila bound for Shenzhen, US–Iran strikes in the Gulf, Bitcoin below $65,000, the US losing measles-free status, Nvidia's earnings amid a spy scandal, and Pattinson as the next James Bond.

## Run it

```sh
python3 main.py
```

## How the image was made

`entry.png` (1024×1024) is a front page composed by `compose.py`: an AI-generated hero illustration of the collapsed Kerch Bridge (`hero-source.webp`) plus headlines rendered with PIL so the text stays pixel-crisp. `main.py` just copies the bundled image to the output path — deterministic, no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=pm33cwks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
