"""The news of Saturday 21 November 2026, as data (v2 — dense front page).

Kept apart from the renderer so the front page can be refreshed with the
full day's news before the deadline (23 Nov 07:00 WIB) by editing this
file alone and re-running draw_poster.py.

Sources (checked 21 Nov 2026 ~09:40 WIB): RFE/RL, political.org,
gsmglobalnews.com, particle.news, snm.rs, ukriotmap.live for the Poland
incursion, Denmark plot and war news; CoinDesk, TradingView, BigGo
Finance, Stocktwits, IBD for the market rout; Reuters + IANS for sport;
wire round-ups for the rest. Every story below is dated 21 Nov 2026 or
late 20 Nov and still the day's news.
"""

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "SATURDAY, 21 NOVEMBER 2026"

KICKER = "WAR SPILLS OVER"
LEAD_TITLE = "POLAND SAYS RUSSIAN MISSILE HIT ITS SOIL"
LEAD_DECK = (
    "Two Russian missiles and a jet-powered drone land in Poland during "
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
        "KYIV BARRAGE KILLS 11 AND HITS THREE BRIDGES",
        "KRYVYI RIH STRIKE KILLS BOY, 7, AND RESCUER; 42 HURT",
        "DENMARK FOILS 'RUSSIAN PLOT' TO KILL RAPPER",
        "ESTONIA TO CLOSE RUSSIAN BORDER FROM DECEMBER 1",
        "EU APPROVES €1BN IN MILITARY AID FOR UKRAINE",
        "KOSOVO EX-PRESIDENT THACI JAILED 17 MONTHS",
        "465 HYBRID ATTACKS LOGGED IN EUROPE IN 90 DAYS",
    )),
    ("ASIA-PACIFIC", "#1f4d7a", (
        "TRUMP, XI AND PUTIN HOLD FIRST TRILATERAL TALKS",
        "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
        "CYCLONE AKVAN FADES OVER ODISHA AFTER LANDFALL",
        "TAIWAN FLAGS CHINA-LINKED ACCOUNTS TO META",
        "NORTH KOREA AND LAOS VOW CLOSER COOPERATION",
        "TALIBAN BANS CRICKET COVERAGE ON KANDAHAR RADIO",
        "INDIAN MAN JAILED 19 YEARS IN US OVER MURDER PLOT",
    )),
    ("MIDDLE EAST", "#8a6d1b", (
        "US–IRAN TIT-FOR-TAT STRIKES GRIND ON",
        "GAZA: 22,000 CHILDREN REPORTED DEAD",
        "HOUTHIS TARGET RIYADH FINANCE TOWER; NO INJURIES",
        "YEMEN DISPLACED RISE TO 357,000 SINCE AUGUST",
        "IRAQ TO DEPLOY TROOPS IN HEZBOLLAH STRONGHOLD",
        "US AND ISRAEL WEIGH FRESH STRIKE ON TEHRAN",
    )),
    ("AMERICAS", "#2e6b34", (
        "BUKELE SEEKS THIRD TERM TO RULE UNTIL 2033",
        "CALIFORNIA SUBPOENAS NVIDIA OVER CHINA CHIP SALES",
        "TRUMP FIRES CYBERSECURITY CHIEF",
        "US OPENS PACIFIC SEABED TO DEEP-SEA MINING",
        "US CURBS MILITARY TIES WITH CANADA",
    )),
    ("AFRICA", "#7a4a1f", (
        "EBOLA HITS CONGO'S CHILDREN; 100 SCHOOLS AFFECTED",
        "MOROCCO PLEDGES €366M FOR HOME DEFENCE INDUSTRY",
    )),
    ("MARKETS", "#3d3d3d", (
        "WALL STREET SUFFERS WORST WEEK SINCE 2020",
        "NASDAQ 100 IN BEAR MARKET, 20% OFF ITS PEAK",
        "BITCOIN BELOW $59,000, LOWEST SINCE SEPTEMBER 2024",
        "ANTHROPIC SLIDES AGAIN AFTER BLOCKBUSTER IPO",
    )),
    ("SPORT & CULTURE", "#1f6b6b", (
        "RAHUL 93* AS INDIA FIGHT BACK IN WELLINGTON",
        "UAE BULLS RETAIN ABU DHABI T10 TITLE",
        "MEDVEDEV BEATS TIAFOE AT ATP FINALS",
        "VOYAGER 1: FIRST OBJECT ONE LIGHT-DAY FROM EARTH",
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
    "Czechia speeds air defence",
    "Tata on trial in the Netherlands",
    "Bayern 1–1 Köln",
    "Hungary lifts EU-talks block",
)

MARKETS_LINE = (
    "MARKETS: BITCOIN $58,333 \u25bc5.1%  \u00b7  ETHER $1,601 \u25bc8%  "
    "\u00b7  S&P 500 \u25bc3.7%  \u00b7  NASDAQ \u25bc5.3%  \u00b7  "
    "GOLD $3,523 \u25bc2.8%"
)

ALSO_LINE = "ALSO: " + "  \u00b7  ".join(ALSO_ITEMS)


def story_count():
    """Lead + grid briefs + footer 'also' items."""
    grid = sum(len(stories) for _, _, stories in REGIONS)
    return 1 + grid + len(ALSO_ITEMS)
