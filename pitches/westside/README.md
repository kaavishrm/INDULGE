# Seen at Westside · Mask360 pitch to Westside

A Zara-app-style HTML pitch from Mask360 to Westside (Trent Ltd), October 2026.

- **Send this file:** `dist/Westside-x-M360-Seen-at-Westside.html`. It is self-contained (about 0.9 MB) with images and logos embedded. It needs an internet connection only for the Google Fonts (Bodoni Moda, Hanken Grotesk); without one it falls back to Georgia and Helvetica.
- **Research behind it:** `reports/Westside marketing audit 2026.md`, with the raw notes in `research_notes/Westside marketing audit 2026/`.

## What's inside

1. The brief: our WhatsApp promise, "from the post to the billing counter"
2. Twelve months of Westside (Oct 2025 to Oct 2026), as a filterable log with sources
3. The gap: "6 million views. How many walked in?"
4. India and Zara: customer truths, and the case for winning where Zara isn't
5. The idea, **Seen at Westside**, and its six IPs: The Trial Room, The Style Collective, The Window, Style Call, First Look and The 72-hour Burst
6. Seventeen visual references across social, content IP, experiential and integrated
7. The journey from post to bill, with the behavioural principle behind each step
8. The pilot as a product page: festive drop or store launch, scope, returns, and what Westside needs to provide
9. The scorecard: a difference-in-differences footfall read and guardrails
10. Scale (1, then 10, then 311+), a 12-month calendar, m360 credentials and the ask

## Editing

Edit `src/body.html` for copy, `src/styles.css` for design and `src/script.js` for data (the 12-month log, journey steps, pilot variants, chart and calendar). Then rebuild:

```
python3 pitches/westside/build.py
```

The build writes two files to `dist/`. `seen-at-westside.html` is the fragment published as the claude.ai artifact. `Westside-x-M360-Seen-at-Westside.html` is the standalone page.

## Check before sending

- **Commercial terms.** The "Returns" section proposes that Mask360's fee is contingent on the agreed footfall threshold, with production and media at cost. Confirm before sending.
- **Store choice.** The mockups use "Westside · Andheri West" (the D.N. Nagar store, where Wesness runs start) as an illustrative pilot store.
- **Visuals.** The store photography is the concept render from the earlier draft. All seventeen mockups are concept frames, and the stylist "Ananya R." is illustrative.
- **Figures.** Several come from secondary coverage of Trent filings; see the report's "unverified" list.
