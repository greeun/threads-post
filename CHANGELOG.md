# Changelog

## [1.1.0] — 2026-06-17

Infographic visualization directive added for image/carousel threads, plus semantic versioning
introduced (`VERSION` + `CHANGELOG.md`).

### Added
- **Infographic visualization (IMAGE / CAROUSEL)** section — when a thread explains something
  structural (process, comparison, architecture, metrics, topic breakdown), attach it as an
  infographic image instead of cramming the 500-char text. Maximize and diversify types (mind map,
  flowchart, architecture, chart/graph, timeline, sequence, webtoon, and other creative
  visualizations beyond the listed types).
- **Plugin-independent standalone images only** — each infographic is a self-contained image
  (PNG/JPG) served from a public URL via `--image-url` (single) or `--carousel-images` (2–20).
  No diagram/chart embed, widget, iframe, or link-preview rendering. `mmdc` → PNG for Mermaid,
  image-gen → PNG for webtoon/custom.
- `VERSION` (1.1.0) and `CHANGELOG.md` introduced.

### Prior unversioned history
- `be73dea` Initial commit: threads-post Claude Code skill
