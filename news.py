"""The news of Saturday 21 November 2026, as data (v4 — headline + SEO round).

Same 40 verified stories as v2/v3 — only the wording changed: headlines
are punchier, tabloid-style hooks (big numbers up front, strong verbs,
curiosity gaps) and today's genuinely trending search terms are woven in
where they fit the story. Every headline stays factually true to its
verified story: sensational wording, never fabricated facts.

Trending terms verified 21 Nov 2026 ~10:05 WIB via Virlo (TikTok/IG,
updated 00:04 UTC), Google Trends round-ups (GlyphSignal, WhatMostSearched,
trends.google.co.in): GTA 6 (dominant everywhere), KL Rahul (#1 global
search), Anthropic IPO, Nasdaq, NVDA, Bayern vs Köln (8 countries),
Robert Pattinson / James Bond, Hunger Games, Russian missiles in Poland,
JPMorgan/Zelle outage. Terms with no matching story on the page live in
the TRENDING NOW footer strip, clearly labelled as the day's searches.

Sources for the stories (checked 21 Nov 2026 ~09:40 WIB): RFE/RL,
political.org, gsmglobalnews.com, particle.news, snm.rs, ukriotmap.live
for the Poland incursion, Denmark plot and war news; CoinDesk,
TradingView, BigGo Finance, Stocktwits, IBD for the market rout; Reuters
+ IANS for sport; wire round-ups for the rest. Every story below is dated
21 Nov 2026 or late 20 Nov and still the day's news.
"""

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "SATURDAY, 21 NOVEMBER 2026"

KICKER = "BREAKING: WAR SPILLS OVER"
LEAD_TITLE = "RUSSIA STRIKES POLAND: NATO ON EDGE"
LEAD_DECK = (
    "Two Russian missiles and a jet-powered drone crash into Poland during "
    "Moscow's barrage on Ukraine; Tusk calls it an 'intentional "
    "provocation' as NATO chief Rutte flies to Warsaw."
)
STATS_LINE = (
    "3 WEAPONS LANDED  ·  11 OBJECTS TRACKED  ·  0 SHOTS FIRED  ·  "
    "F-16s & GRIPENS SCRAMBLED"
)

# (region, colour, headlines) — headlines are self-contained briefs.
REGIONS = (
    ("EUROPE", "#7a1f1f", (
        "KYIV UNDER FIRE: 11 DEAD AS 3 BRIDGES BLASTED",
        "KRYVYI RIH HORROR: BOY, 7, KILLED; 42 WOUNDED",
        "DENMARK FOILS 'RUSSIAN PLOT' TO ASSASSINATE RAPPER",
        "ESTONIA SLAMS SHUT ITS RUSSIAN BORDER ON DEC 1",
        "EU UNLEASHES €1BN WAR CHEST FOR UKRAINE",
        "THACI JAILED: EX-PRESIDENT GETS 17 MONTHS",
        "465 SHADOW ATTACKS HIT EUROPE IN JUST 90 DAYS",
    )),
    ("ASIA-PACIFIC", "#1f4d7a", (
        "TRUMP, XI, PUTIN IN FIRST-EVER 3-WAY SUMMIT",
        "WORLD COURT: MYANMAR GUILTY OF ROHINGYA GENOCIDE",
        "CYCLONE AKVAN SLAMS ODISHA — THEN LOSES ITS PUNCH",
        "TAIWAN EXPOSES CHINA-LINKED ACCOUNTS TO META",
        "KIM'S NORTH KOREA FORGES CLOSER TIES WITH LAOS",
        "TALIBAN SILENCES CRICKET ON KANDAHAR RADIO",
        "19 YEARS FOR MURDER PLOT: INDIAN MAN JAILED IN US",
    )),
    ("MIDDLE EAST", "#8a6d1b", (
        "US–IRAN MISSILE WAR GRINDS INTO MONTH 9",
        "GAZA HORROR: 22,000 CHILDREN REPORTED DEAD",
        "HOUTHI MISSILES TARGET RIYADH — ALL SHOT DOWN",
        "YEMEN EXODUS: 357,000 FLEE SINCE AUGUST",
        "IRAQ SENDS TROOPS INTO HEZBOLLAH STRONGHOLD",
        "TEHRAN IN THE CROSSHAIRS AS US, ISRAEL WEIGH STRIKE",
    )),
    ("AMERICAS", "#2e6b34", (
        "BUKELE BIDS FOR THIRD TERM — POWER UNTIL 2033",
        "CALIFORNIA SUBPOENAS NVIDIA — NVDA IN THE DOCK",
        "TRUMP SACKS CYBER CHIEF AMID US OUTAGE CHAOS",
        "PACIFIC SEABED THROWN OPEN TO DEEP-SEA MINING",
        "US SNUBS CANADA — MILITARY TIES CURBED",
    )),
    ("AFRICA", "#7a4a1f", (
        "EBOLA STALKS CONGO'S CHILDREN AS 100 SCHOOLS HIT",
        "MOROCCO BETS €366M ON HOME-GROWN ARMS INDUSTRY",
    )),
    ("MARKETS", "#3d3d3d", (
        "WALL STREET BLEEDS: WORST WEEK SINCE 2020",
        "NASDAQ 100 CRASHES INTO BEAR MARKET — DOWN 20%",
        "BITCOIN CRASH: BELOW $59K, LOWEST SINCE SEPT 2024",
        "ANTHROPIC SLIDES AGAIN AS IPO EUPHORIA FADES",
    )),
    ("SPORT & CULTURE", "#1f6b6b", (
        "KL RAHUL'S 93* DRAGS INDIA BACK IN WELLINGTON",
        "UAE BULLS STORM TO BACK-TO-BACK ABU DHABI T10 TITLE",
        "MEDVEDEV DOWNS TIAFOE AT THE ATP FINALS",
        "VOYAGER 1 MAKES HISTORY: ONE LIGHT-DAY FROM EARTH",
    )),
)

# Which regions go in which of the three columns, top to bottom.
# Balanced by measured height so no column overflows the grid.
COLUMNS = (
    ("EUROPE", "MARKETS"),
    ("ASIA-PACIFIC", "AFRICA", "SPORT & CULTURE"),
    ("MIDDLE EAST", "AMERICAS"),
)

# Short items for the footer's second line (also counted in the total).
# Kept short so the line fits on one line at 15px.
ALSO_ITEMS = (
    "Czechia boosts air defence",
    "Tata on trial in Netherlands",
    "Bayern held 1–1 by Köln",
    "Hungary ends EU-talks block",
)

MARKETS_LINE = (
    "MARKETS: BITCOIN $58,333 \u25bc5.1%  \u00b7  ETHER $1,601 \u25bc8%  "
    "\u00b7  S&P 500 \u25bc3.7%  \u00b7  NASDAQ \u25bc5.3%  \u00b7  "
    "GOLD $3,523 \u25bc2.8%"
)

ALSO_LINE = "ALSO: " + "  \u00b7  ".join(ALSO_ITEMS)

# The day's most-searched terms (verified, see module docstring). These
# are what the world is searching for — not stories on this page.
TRENDING_LINE = (
    "TRENDING NOW: GTA 6  \u00b7  KL RAHUL  \u00b7  ANTHROPIC IPO  "
    "\u00b7  NASDAQ  \u00b7  BITCOIN  \u00b7  JAMES BOND  \u00b7  "
    "HUNGER GAMES"
)


def story_count():
    """Lead + grid briefs + footer 'also' items."""
    grid = sum(len(stories) for _, _, stories in REGIONS)
    return 1 + grid + len(ALSO_ITEMS)
