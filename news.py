"""The news of Saturday 21 November 2026, as data.

Kept apart from the renderer so the front page can be refreshed with the
full day's news before the deadline (23 Nov 07:00 WIB) by editing this
file alone and re-running draw_poster.py.

Sources (checked 21 Nov 2026 ~09:35 WIB): RFE/RL and wire round-ups for
the Poland missile report, the Shenzhen trilateral and the ICJ verdict;
WSJ, CoinDesk and TradingView for the Bitcoin sell-off; IMD advisories
for Cyclone Akvan; COP31 wire coverage.
"""

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "SATURDAY, 21 NOVEMBER 2026"

KICKER = "WAR SPILLS OVER"
LEAD_TITLE = "POLAND SAYS RUSSIAN MISSILE HIT ITS SOIL"
LEAD_DECK = (
    "Warsaw reports a missile strike during Moscow's barrage on Ukraine "
    "and asks NATO for support; Danish jets scramble as an explosion is "
    "reported near the border."
)

# How the day unfolded: three steps, left to right.
TIMELINE = (
    ("SHENZHEN SUMMIT",
     "Trump, Xi and Putin hold first-ever trilateral talks"),
    ("STRIKES ON KYIV",
     "Russian barrage kills at least 11 across Ukraine"),
    ("MISSILE IN POLAND",
     "Warsaw reports a strike on its soil, seeks NATO help"),
)

# (headline, deck) — two-column grid, in reading order.
STORIES = (
    (
        "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "First-ever trilateral talks at the APEC summit end with a "
        "four-point declaration on the war in Ukraine.",
    ),
    (
        "ICJ: MYANMAR COMMITTED GENOCIDE",
        "World court rules Myanmar responsible for genocide against "
        "the Rohingya; Myanmar and China reject the verdict.",
    ),
    (
        "BITCOIN SINKS BELOW $59,000",
        "Lowest since September 2024 as the AI-stock rout spills into "
        "crypto; $1.5bn in leveraged bets wiped out in a day.",
    ),
    (
        "COP31 TALKS RUN INTO OVERTIME",
        "Climate negotiators push past their deadline with fossil-fuel "
        "language still unresolved and no deal in sight.",
    ),
)

WIDE_TITLE = "AKVAN FADES OVER ODISHA"
WIDE_DECK = (
    "Cyclone weakens to a depression after landfall near Gopalpur; "
    "heavy rain spreads inland to Bengal, Bihar and Assam."
)

FOOTER_LINES = (
    "MARKETS: BITCOIN $58,317 \u25bc  \u00b7  ETHER \u22127.6%  \u00b7  "
    "NASDAQ \u22123.8%  \u00b7  GOLD $3,500",
    "ALSO: EU pledges \u20ac1bn in military aid to Ukraine  \u00b7  "
    "US\u2013Iran tit-for-tat strikes continue",
)
