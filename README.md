# Voltavia

Marketing site for Voltavia electric scooters. Plain HTML, CSS and vanilla
JavaScript. No framework, no build step, no dependencies.

## What is here

| Path | What it is |
|---|---|
| `index.html` | The site. Everything except the images. |
| `assets/` | Product photography, WebP with alpha. |
| `voltavia-standalone.html` | Generated single file with every image inlined as base64. For sending to people. |
| `tools/build-standalone.py` | Regenerates the standalone file from `index.html` + `assets/`. |

## Running it locally

The page loads fine from a double click, but serve it if you want to be sure
everything behaves the way it will on a host:

```
python -m http.server 8817
```

Then open <http://127.0.0.1:8817/>.

## Rebuilding the standalone file

Run this after any change to `index.html` or `assets/`, or the shareable copy
goes stale:

```
python tools/build-standalone.py
```

## How the page is built

- **Scroll hero.** A pinned 530vh region maps scroll progress to 0..1. That
  progress drives the flagship's transform and four caption bands that cross
  fade through it. The loop is `requestAnimationFrame` and it rests once it
  converges, so it costs nothing while you are reading.
- **Static hero.** Phones, portrait tablets, coarse pointer devices, short
  landscape phones and reduced motion get a composed still hero instead. The
  five conditions are identical in the CSS and in the JS, and they are wired to
  `change` listeners so rotating the device or flipping the motion preference
  swaps modes live in both directions.
- **Press and hold.** The battery section has one interactive moment. Hold the
  button and fourteen cells fill; let go early and the charge eases back rather
  than snapping to zero; reaching 100% reveals the three pack formats.
- **Legibility.** Every hero band carries a global scrim, a per band scrim that
  deepens with the band, and a three layer text shadow.

## Verified

Checked in headless Chrome, not assumed:

- Zero console errors, zero horizontal overflow at 1440, 390 and 375 wide.
- Hero text worst pixel contrast 17:1 against a 3.5:1 floor.
- Flick test passes: every caption readable for 5 to 6 normal scroll flicks,
  none skippable at 360px steps.
- Static hero gates and reduced motion both verified with real touch and media
  emulation.
- All 15 images load from `file://` in the standalone build.

## Known gaps

These need real values from the product catalogue before the site goes public:

1. **Model names.** The source PDF used subset embedded fonts whose glyph
   encoding could not be decoded, so the ten model names are placeholders named
   after their finish (Arctic Blue, Crimson, Blush Lima, and so on).
2. **Specifications.** The figures on the flagship were recovered from that same
   scrambled text layer and should be confirmed against the catalogue.
3. **Battery variants.** Only the 60V 32Ah pack has real figures. The compact and
   extended packs are described without numbers on purpose.

## Deploying

Any static host serves this. The repository root is the web root, so GitHub Pages
works with no configuration. Before going live, patch the two absolute URLs at
the `<!-- DEPLOY STEP -->` comment in `index.html`:

```html
<meta property="og:url" content="https://example.com/">
<meta property="og:image" content="https://example.com/assets/hero-tranz.webp">
```
