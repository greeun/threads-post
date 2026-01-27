#!/usr/bin/env python3
"""Threads API post publisher.

Supports TEXT, IMAGE, and CAROUSEL posts via Meta Threads API.
Supports replies (comments) to existing posts up to 3 levels deep.
Uses two-step flow: create container → publish.

Environment variables:
    THREADS_ACCESS_TOKEN: Long-lived access token
    THREADS_USER_ID: Threads user ID
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://graph.threads.net/v1.0"


def api_request(endpoint, params=None, method="POST"):
    """Make API request to Threads."""
    url = f"{BASE_URL}/{endpoint}"
    if params is None:
        params = {}

    token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not token:
        print("ERROR: THREADS_ACCESS_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    params["access_token"] = token

    data = urllib.parse.urlencode(params).encode("utf-8")

    if method == "GET":
        url = f"{url}?{data.decode('utf-8')}"
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(url, data=data)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code} - {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}", file=sys.stderr)
        sys.exit(1)


def get_user_id():
    """Get user ID from env or API."""
    uid = os.environ.get("THREADS_USER_ID")
    if uid:
        return uid
    result = api_request("me", {"fields": "id"}, method="GET")
    return result["id"]


def create_text_container(user_id, text, reply_to_id=None):
    """Create a TEXT media container."""
    params = {
        "media_type": "TEXT",
        "text": text,
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
    return api_request(f"{user_id}/threads", params)


def create_image_container(user_id, text, image_url, reply_to_id=None):
    """Create an IMAGE media container."""
    params = {
        "media_type": "IMAGE",
        "image_url": image_url,
        "text": text,
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
    return api_request(f"{user_id}/threads", params)


def create_carousel_item(user_id, media_type, media_url):
    """Create a single carousel item container."""
    params = {
        "media_type": media_type,
        "is_carousel_item": "true",
    }
    if media_type == "IMAGE":
        params["image_url"] = media_url
    elif media_type == "VIDEO":
        params["video_url"] = media_url
    return api_request(f"{user_id}/threads", params)


def create_carousel_container(user_id, text, children_ids, reply_to_id=None):
    """Create a CAROUSEL media container."""
    params = {
        "media_type": "CAROUSEL",
        "text": text,
        "children": ",".join(children_ids),
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
    return api_request(f"{user_id}/threads", params)


def publish_container(user_id, creation_id):
    """Publish a media container."""
    return api_request(f"{user_id}/threads_publish", {
        "creation_id": creation_id,
    })


def wait_for_media_ready(seconds=30):
    """Wait for media processing."""
    print(f"Waiting {seconds}s for media processing...", file=sys.stderr)
    time.sleep(seconds)


def main():
    parser = argparse.ArgumentParser(description="Publish to Threads")
    parser.add_argument("--text", required=True, help="Post text (max 500 chars)")
    parser.add_argument("--image-url", help="Public image URL for IMAGE post")
    parser.add_argument(
        "--carousel-images",
        help="Comma-separated public image URLs for CAROUSEL (2-20 items)",
    )
    parser.add_argument(
        "--reply-to",
        help="Media ID of the post/comment to reply to (up to 3 levels deep)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print payload without publishing")

    args = parser.parse_args()

    text = args.text
    if len(text) > 500:
        print(f"WARNING: Text is {len(text)} chars (max 500). Will be truncated by API.", file=sys.stderr)

    if args.dry_run:
        payload = {"text": text, "media_type": "TEXT"}
        if args.carousel_images:
            urls = [u.strip() for u in args.carousel_images.split(",")]
            payload["media_type"] = "CAROUSEL"
            payload["children"] = [{"media_type": "IMAGE", "image_url": u} for u in urls]
        elif args.image_url:
            payload["media_type"] = "IMAGE"
            payload["image_url"] = args.image_url
        if args.reply_to:
            payload["reply_to_id"] = args.reply_to
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    user_id = get_user_id()

    reply_to = args.reply_to

    if args.carousel_images:
        urls = [u.strip() for u in args.carousel_images.split(",")]
        if len(urls) < 2 or len(urls) > 20:
            print("ERROR: Carousel requires 2-20 items", file=sys.stderr)
            sys.exit(1)
        children_ids = []
        for url in urls:
            result = create_carousel_item(user_id, "IMAGE", url)
            children_ids.append(result["id"])
            print(f"  Created carousel item: {result['id']}", file=sys.stderr)
        wait_for_media_ready()
        container = create_carousel_container(user_id, text, children_ids, reply_to)
    elif args.image_url:
        container = create_image_container(user_id, text, args.image_url, reply_to)
        wait_for_media_ready()
    else:
        container = create_text_container(user_id, text, reply_to)

    creation_id = container["id"]
    print(f"Container created: {creation_id}", file=sys.stderr)

    # Brief wait for text-only posts too
    if not args.image_url and not args.carousel_images:
        time.sleep(3)

    result = publish_container(user_id, creation_id)
    post_id = result["id"]
    print(f"Published: {post_id}", file=sys.stderr)
    print(json.dumps({"post_id": post_id, "status": "published"}, indent=2))


if __name__ == "__main__":
    main()
