# The Park Hotels × Mask360 · proposal

Prepared 17 October 2026 for Anmol Tyagi (Senior Manager, Brand, The Park Hotels), in reply to his LinkedIn call for social media agencies.

**The deck:** [The Park Hotels × Mask360](https://claude.ai/artifact/7iHP59dK2NgHFLfiwzWX4e), 23 slides. It is private until shared from the page's Share menu.

**The idea in one line:** The Park is named after a street. *Park Street, everywhere*: each THE Park hotel becomes the Park Street of its city, told through a magazine of its nights.

**The look:** Mask360's house proposal style, from the Westside v4 deck (`claude/wizardly-bardeen-2oc2qq`, `pitches/westside/v4/`). It uses white paper and black ink, thin uppercase Inter Tight, Bodoni only for numbers, hairline rules, procedural cloth, line drawings and the m360 mark. The kit (`deck.css`, `deck.js`, `fabric.js`, `kit.py`, the fonts) is copied from that deck. The Park's corporate mark (`deck/park.svg`, taken from https://www.theparkhotels.com/images/site-specific/park-corporate-logo.svg) sits in the running heads, on the cover and on the close, drawn in each slide's ink. `fetch_logo.py` and the `park-logo` workflow fetch it again if it changes, since the coding sandbox cannot reach theparkhotels.com.

- **Present:** open the link full screen and use the arrow keys or the space bar. On a phone, the slides become one scrolling page.
- **Print or PDF:** printing `dist/index.html` from a browser gives one slide per page.

## The slides

A social media pitch in 26 slides. The content plan is drawn as two mind maps.

1. **Cover, our promise, your brief.** The promise: THE Park's feed becomes the city's night out (found, saved, booked). The brief table answers the four things the post asked for, each with its page.
2. **01 · The Park on social.**
   - The numbers the feed has to sell: 92% occupancy, 43% of revenue from food and nightlife, RevPAR ₹6,858, 42 hotels, 87 by FY2030, 111 Flurys.
   - The six channels linked from theparkhotels.com, each with a job and a weekly cadence, plus Spotify and WhatsApp.
   - The house rule: "We post what only THE Park can."
3. **The insight:** The Park is named after a street.
4. **02 · Park Street, everywhere.**
   - **The content map:** a mind map with the idea at the centre, four pillars (After Hours, By Design, The Table, The City) and sixteen series with their formats.
   - The pillar mix.
   - The first fortnight of December on the @theparkhotels grid, drawn as a phone.
   - Sample captions and three voice rules.
   - Three series pages with concept drawings: The Sessions (with sample posts), Room 1967 and Flurys 100.
5. **03 · How it runs.**
   - December on the feed: a calendar of the series day by day, with Christmas on Park Street and New Year's Eve.
   - **The handle map:** a second mind map, the group feed and the six brand accents.
   - Community (residents, regulars, creators, the DMs), post to table, and social KPIs.
6. **Mask360**, next steps ("Put us in the room."), the close and the sources.

Mask360's rule for cold pitches applies: show the read, take one position, show how it extends into a system, and end on an open door. So there is no pricing and no team grid.

## Building

```
STRICT=1 python3 pitches/the-park-hotels/deck/build.py
```

- `deck/content.py` holds the slide copy and layout. Page references in the brief table are looked up from `ORDER`.
- `deck/art.py` holds the line drawings: the stage, the suite, the cup and pastry box, the hotel grid and the sample-post phones.
- The build writes `dist/the-park-proposal.html` (the claude.ai artifact) and `dist/index.html` (the standalone page).
- `STRICT=1` fails the build on:
  - em or en dashes;
  - contrast constructions ("X, not Y", "rather than", "instead of");
  - filler words;
  - exclamation marks;
  - leftover placeholders.

## Before sending

- **Share the link.** The artifact is private until shared. To send a website link like the Westside one (`mask360westside`), the same EdgeOne deploy can be added for this deck. It has not been set up.
- **Client names on slide 20.** These are taken from Kaavish's credentials notes: Anantara Jewel Bagh, The St. Regis Mumbai, Moxy Mumbai, Alta Stella, Onrique and DEA, Atlantis The Royal and SANA, the Penthouse and Moxy feeds, the Nexa Platinum Lounge result, and Dior, Ferrari India, L'Oréal, Dyson and Lollapalooza India. Confirm permission to name each one in a pitch; his notes say press uses career framing because of NDAs.
- **Contact details on slide 21:** kaavish@mask360.agency, +91 959 107 5100, mask360.agency, mask360.work. Confirm they are the ones to show.
- **The house rule (slide 8).** Check the last 30 posts on @theparkhotels. If any "what most hotel feeds post" item appears there, swap it out, so the slide doesn't criticise the team it is written to.
- **The Sessions.** The deck says bands play original songs and sign a release, with no drinks brands in frame. Keep that, because full sets on YouTube need music rights.
- **Dates** assume a start on Monday 16 November 2026. The literary festival row assumes the group's festival team agrees.
- **Growth figure.** 87 hotels by FY2030 is the company's latest (Q1 FY27 material and the 2 Sep 2026 investor meet filing). It replaces the 85 from an earlier Priya Paul interview.

## Research: what matters about The Park

**Company and brand**
- Founded 1967 with The Park Kolkata on Park Street; the group's name comes from the street. Priya Paul (chair since about 1990) began the design repositioning in 1992. THE Park Bangalore (2000) was designed by Terence Conran. Six hotels are long-time Design Hotels members.
- "Anything But Ordinary" has been the line since the 2013 rebrand.
- Five hotel brands: **THE Park**, **THE Park Collection**, **Zone by The Park** (design-conscious and price-conscious, second cities), **Zone Connect by The Park**, **Stop by Zone**. The group also owns **Flurys**.
- 42 hotels in 32 cities (Business Traveller, Oct 2026). The company's latest target is **87 hotels and 6,719 keys by FY30**, with 45 hotels under development. Priya Paul says five THE Park hotels are under construction.

**Performance (Q1 FY27, quarter to 30 June 2026)**
- Revenue from operations ₹166.8 crore, up 8.1%. PAT ₹11.5 crore, down 14.2%.
- Occupancy **92%**. RevPAR about **₹6,858**. Sources disagree on ARR (₹7,459 against ₹9,310); ₹7,459 is consistent with RevPAR.
- Food, beverage, nightlife and lifestyle dining about **43% of revenue** (IDBI Capital).
- Management guides to high single-digit ARR growth.

**Growth and pipeline**
- March 2026: Zone by The Park Darjeeling, Zone Connect Gangtok and Zone Connect Katra opened. Zone Connect Patna opened in January 2026.
- Signed: Zone Connect Ayodhya (56 rooms) and Ujjain (64 rooms), April 2026; Zone Connect Bharatpur (63 keys), HMA filed with NSE on 28 Sep 2026; THE Park in a Siliguri tea estate (100 rooms); THE Park Juhu, Mumbai (due mid-2027); The Park Unizen with Ambuja Neotia (Feb 2026).
- **Ran Baas The Palace, Patiala** (THE Park Collection) opened January 2025: 35 suites, named among the world's most beautiful hotels of 2025 by Prix Versailles.
- **Flurys**: 111 stores (Q1 FY27). First standalone North India café, open 24 hours, in Gurugram (7 Aug 2026). Targeting 130 to 140 outlets by FY27 and about 300 later. **Centenary in 2027.**

**Venues**
- Kolkata: Someplace Else (live-music pub), Tantra (two-floor nightclub), Roxy, Zen, Aqua.
- New Delhi (Connaught Place): Aqua, Fire, Agni.
- Hyderabad: Aish.
- Group-run culture in Kolkata: the Park Street Christmas festival (co-organised by the Apeejay Surrendra Group) and the Apeejay Kolkata Literary Festival in January.

**Social and audience context**
- Last public snapshots found: @theparkhotels about 28K Instagram followers (about 2024), Facebook about 113K, LinkedIn about 84K. Check live numbers before quoting any of these.
- Booking.com, via Outlook Traveller: 80% of Indian travellers plan to spend most of their time at the property, against 51% globally.

## Outreach

This follows Kaavish's BD flow: a LinkedIn DM in proper case, then a cold email in two variants under 100 words. Each opens on a specific observation, with no self-introduction.

**LinkedIn DM**

> Anmol, The Park took its name from Park Street, Calcutta's night out. We built our reply around that: Park Street, everywhere. Someplace Else filmed in one take every month, one suite a year remade by a young Indian designer, and Flurys at 100. It is 23 pages, with the hospitality work behind it: [link]. Thirty minutes with your team would be enough to walk through it.
>
> Kaavish Ramchandani, Mask360

**Email, variant A (recommended: it opens on the observation)**

> Subject: Park Street, everywhere
>
> Hi Anmol,
>
> The Park took its name from a street. Park Street was where Calcutta went out, and Someplace Else, Tantra and Agni still carry that scene.
>
> Our reply to your call for agencies builds on it: each THE Park becomes the Park Street of its city. At 92% occupancy, growth comes from rate, tables and 45 new hotels, so we measure covers and direct bookings.
>
> The 23-page point of view: [link]
>
> Could we have thirty minutes with the brand team?
>
> Kaavish

**Email, variant B (numbers first)**

> Subject: 92% full, and 45 hotels to open
>
> Hi Anmol,
>
> At 92% occupancy, THE Park grows through rate, tables and 45 new hotels. That calls for social built around nights and measured in covers and direct bookings.
>
> Our point of view, in reply to your call for agencies: Park Street, everywhere, with The Sessions at Someplace Else and Flurys at 100. [link]
>
> Thirty minutes with the brand team?
>
> Kaavish

## Sources

- [Apeejay Surrendra Park Hotels Q1 FY27 results (Investywise)](https://www.investywise.com/apeejay-surrendra-park-hotels-limited-q1-fy27-financial-results/)
- [Q1 FY27: 92% occupancy, Flurys plans (ScanX)](https://scanx.trade/stock-market-news/companies/apeejay-surrendra-park-hotels-q1-results-net-profit-falls-14-yoy-115/48449041)
- [Q1 FY27 result review (IDBI Capital)](https://www.idbidirect.in/IDBIAdmin/Pdf/PARKHOTE_RR_19082026-19-August-2026-1444990745.pdf)
- [Q1 FY27: keys and the 87-hotel portfolio (Multibagg)](https://www.multibagg.ai/market-pulse/articles/parkhotels-q1fy27-98354)
- [Management meet update (PL Capital)](https://plindia.com/ResReport/PARKHOTE-10-9-26-PL.pdf)
- [Zone Connect Bharatpur HMA, filing to NSE, 28 Sep 2026](https://nsearchives.nseindia.com/corporate/ASPHL_28092026130940_Intimation.pdf)
- [Three new properties, portfolio at 39 (BW Hotelier)](https://www.bwhotelier.com/article/apeejay-surrendra-park-hotels-launches-three-new-properties-600985)
- [Ayodhya and Ujjain (Construction World)](https://www.constructionworld.in/policy-updates-and-economic-news/apeejay-surrendra-park-hotels-expands-into-ayodhya-and-ujjain/90373)
- [Flurys' first standalone café in Gurugram (Sahi)](https://www.sahi.com/news/apeejay-surrendra-park-hotels-launches-first-standalone-flurys-caf-in-gurugram-3391-PE1_COR)
- [Priya Paul: "Luxury should be anything but boring" (Business Traveller)](https://www.businesstraveller.com/insights/interviews/luxury-should-be-anything-but-boring-hotelier-priya-paul-on-disruption-empowerment-and-restoring-the-palace/)
- [BTN interviews Priya Paul](https://www.breakingtravelnews.com/focus/article/btn-interviews-priya-paul-on-reinventing-indian-hospitality-the-park-hotels/)
- [Ran Baas The Palace (Robb Report India)](https://www.robbreportindia.com/travel/india/a-royal-revival-in-the-heart-of-patiala)
- [The Park Hotels corporate overview](https://www.theparkhotels.com/corporate-information.html)
- [50 years of The Park Hotels (Hotel Designs)](https://hoteldesigns.net/industry-news/50-years-young-the-park-hotels-and-the-woman-behind-the-brand/)
- [Meeting Priya Paul (Sleeper)](https://www.sleepermagazine.com/stories/editorial/meeting-priya-paul/)
- [2013 rebrand, "Anything But Ordinary" (Travel Trends Today)](https://www.traveltrendstoday.in/the-park-hotels-unveils-new-brand-identity)
- [Zone by The Park launch (eHotelier)](https://insights.ehotelier.com/news/2015/01/13/new-design-hotel-brand-zone-by-the-park-launches-in-india/)
- [THE Park Kolkata dining](https://www.theparkhotels.com/kolkata/dining/)
- [Delhi Tourism: THE Park New Delhi](https://delhitourism.gov.in/dt/stay_in_delhi/the_park_new_delhi.html)
- [Kolkata Christmas festival on Park Street (News Arena)](https://www.newsarenaindia.com/states/kolkata-lights-up-with-christmas-festivities-on-park-street/31345)
- [17th Apeejay Kolkata Literary Festival (t2online)](https://t2online.in/goodlife/books/the-17th-apeejay-kolkata-literary-festival-will-be-held-at-the-alipur-museum-from-january-9-to-11--2026/2002616)
- [How Gen Z is redefining travel, Booking.com figure (Outlook Traveller)](https://www.outlooktraveller.com/News/india-travels-differently-now)
- [@theparkhotels on Instagram](https://www.instagram.com/theparkhotels/)
