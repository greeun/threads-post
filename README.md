# threads-post

A Claude Code skill that uses the Meta Threads API. With natural-language commands it handles writing Threads posts, publishing images/carousels, and posting comments/replies.

## Features

- **TEXT** — Text post
- **IMAGE** — Text + 1 image (public URL, max 8MB)
- **CAROUSEL** — Text + 2–20 images
- **Comments/replies** — Up to 3 levels deep via `reply_to_id`

## Structure

```
threads-post/
├── SKILL.md                    # Skill definition (workflow, constraints)
├── scripts/
│   └── publish_thread.py       # Threads API publishing script
└── references/
    └── post-templates.md       # Post templates by use case
```

## Prerequisites

### 1. Meta Developer Portal Setup

1. Create a Business app in the [Meta Developer Portal](https://developers.facebook.com/)
2. Add the Threads product
3. Scopes: `threads_basic`, `threads_content_publish`
4. OAuth authentication → short-lived token → exchange for a long-lived token

### 2. Environment Variables

```bash
export THREADS_ACCESS_TOKEN="your-long-lived-access-token"
export THREADS_USER_ID="your-threads-user-id"  # optional
```

### 3. Register the Skill with Claude Code

```bash
ln -s /path/to/threads-post ~/.claude/skills/threads-post
```

## Usage

### Use in Claude Code with Natural Language

```
# Tech content
오늘 Python match 문 배운 거 쓰레드에 올려줘

# Brand promotion
WithWiz v2.0 업데이트 발표 쓰레드 써줘

# Educational content
FastAPI 강의 소개 쓰레드 포스트 써줘

# Comment
포스트 18050206876707110에 댓글 달아줘

# Reply
댓글 18099887766554433에 대댓글 달아줘
```

### Run the Script Directly

```bash
# Text post
python3 scripts/publish_thread.py --text "Post content"

# Image post
python3 scripts/publish_thread.py --text "Content" --image-url "https://example.com/img.jpg"

# Carousel post
python3 scripts/publish_thread.py --text "Content" \
  --carousel-images "https://example.com/1.jpg,https://example.com/2.jpg"

# Comment
python3 scripts/publish_thread.py --text "Comment" --reply-to "media-ID"

# Dry run
python3 scripts/publish_thread.py --text "Test" --dry-run
```

### Options

| Option | Description | Required |
|------|------|------|
| `--text` | Post text (max 500 chars) | O |
| `--image-url` | Public image URL | X |
| `--carousel-images` | Carousel image URLs (comma-separated) | X |
| `--reply-to` | Target media ID for the reply | X |
| `--dry-run` | Inspect the payload without publishing | X |

## Templates by Use Case

| Use case | Templates |
|------|--------|
| Tech content | TIL, tech tips, tool recommendations |
| Work session summary | Dev logs, problem-solving records |
| Company/brand promotion | Product intros, update announcements, events, customer stories |
| Educational content | Course intros, workshop notices, roadmaps, student reviews |
| General | Sharing opinions, sharing links |

For detailed templates, see `references/post-templates.md`.

## API Constraints

- 500-character limit
- 1 hashtag
- 250 posts within 24 hours
- Public image URL required (max 8MB)
- 2–20 carousel images
- Comment depth up to 3 levels
- Publishing fails if there are more than 5 links

## Dependencies

Uses only the Python 3 standard library. No additional packages required.

## License

MIT
