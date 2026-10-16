# Seen at Westside · Mask360 pitch to Westside

A Zara-app-style HTML pitch from Mask360 to Westside (Trent Ltd), October 2026. Version 3.

- **Send this file:** `dist/Westside-x-M360-Seen-at-Westside.html`. It is self-contained (about 0.9 MB), with images, logos and fonts embedded, and works offline.
- **Research behind it:**
  - `reports/Westside marketing audit 2026.md`, with its notes in `research_notes/Westside marketing audit 2026/`.
  - `research_notes/Zara and Target content IP/`: Zara's content properties, its app and UI, @TargetStyle as a style account, and Target's creator programmes. Each note ends with a verification table.

## What's inside (30 screens, each with DETAILS +)

1. **The brief.** Our WhatsApp promise, "from the post to the billing counter".
2. **Westside today.** Store count and sales mix, a 13-moment log of the last twelve months, the Indian shopper, and the gap with Zara.
3. **The idea.**
   - *Every look has an address.*
   - **@seenatwestside**, a dedicated style account built the way @TargetStyle is: a profile mock-up, the weekly rhythm and the launch.
   - A reference screen on what we take from Zara and from Target Style.
4. **The IPs.** Eight properties, each shown as a product page:
   - Mausam
   - The Window
   - The Trial Room
   - Seen In
   - First Look
   - Dehleez
   - Five Functions
   - The Regulars

   Also a 52-week glass calendar and four of the fourteen art-direction rules.
5. **The store.** The post-to-bill tracker, nine in-the-wild mock-ups, and the WhatsApp operations behind HOLD and BOOK.
6. **The pilot.** One opening for eight weeks (store launch recommended, festive drop as the alternative), returns, what we need, and a scorecard with a read for a launch and a read for an existing store.
7. **Scale, Mask360 and the ask.** The ask is a checkout pre-filled with the recommended pilot.

## Editing

Sources are in `src/`:

- `build3.py` holds the screen copy and assembles the page.
- `ips.py` holds the eight property screens.
- `ipsheets.json` holds their Details sheets.
- `account.json` holds the style account and its Target Style evidence.
- Styles are in `deck3.css`, `extra3.css` and `mock.css`.
- Behaviour is in `deck3.js`, `extras3.js` (the log data) and `fabric.js` (the rendered textiles).

Rebuild with:

```
STRICT=1 python3 pitches/westside/build.py
```

`STRICT=1` makes the build fail if internal research notes, placeholders or a wrong handle reach the page. The build writes two files to `dist/`:

- `seen-at-westside.html` is the fragment published as the claude.ai artifact.
- `Westside-x-M360-Seen-at-Westside.html` is the standalone page.

## Before sending

- **Commercial terms.** The pilot promises no agency fee unless verified footfall beats the comparison by an agreed threshold, with production and media at cost "within a cap agreed before launch". Add the cap, the fee and the names of the pilot team.
- **Handle.** Check that @seenatwestside (fallback @westsidestyle) is free on Instagram, YouTube and Threads, and reserve it.
- **Feed audit.** The research could not open Instagram. Before the meeting, review 90 days of @westsidestores Reels, highlights and YouTube. If a Diwali 2025 film or store-named posts turn up, edit the Oct '25 log card and the gap line.
- **Figures to confirm.**
  - YNG as a 4,000-member community: check the Trent Q4 FY26 investor presentation (BSE filing).
  - Umashan Naidoo's title before he is proposed as house creative director.
- **Client list.** AJIO Luxe belongs to Reliance Retail, a Westside competitor. Decide whether it stays on the Mask360 screen.
- **Visuals.** All visuals are mock-ups: rendered fabrics, interface frames, crops of one concept store render and three styling frames. Real styling photography (looks on Indian bodies for Mausam, The Window, The Trial Room, Five Functions and Seen In) would lift the deck most.
- **Dates and numbers.** 2027 festival and wedding dates follow the published calendar and must be fixed with Trent. First Look No. 330 is an illustrative opening number. Store names in the mock-ups are illustrative.
- **Positioning.** Zara and Target are named only inside this pitch, never in consumer copy, and the deck says it is not affiliated with Zara/Inditex or Target.
